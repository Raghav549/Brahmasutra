"""🕉️ ब्रह्म-LLM के परीक्षण — every claim in ``docs/LLM.md`` has a check here.

The important ones are the numerical proofs (gradients against central
differences, सूत्र-VM forward pass against the Python one) and the safety gates
(a corrupt kernel image cannot be installed, a broken program cannot enter the
corpus, a self-edit that changes predictions is rejected).
"""

from __future__ import annotations

import json
import math
import os

import pytest

from brahma_llm.app_builder import generate_app, slug
from brahma_llm.kernel import (
    IMAGE_SIGNATURE, boot, build_image, install, read_image, unpack_image, verify,
)
from brahma_llm.model import BrahmaLLM, NeuralLM, NgramLM
from brahma_llm.programs import (ProgramGenerator, load_corpus, sutra_files,
                                 validate_program)
from brahma_llm.selfedit import SelfEditor, expand_hidden, shrink_hidden
from brahma_llm.sutra_kernel import SUTRA_MATH, SutraKernel, compare, self_check
from brahma_llm.tokenizer import SutraTokenizer, aksharas


SMALL_CORPUS = [
    'दर्शय "नमस्ते विश्व"\n',
    "स्थापय अ = १०\nदर्शय अ + ५\n",
    "कार्य योग(a, b)\n    प्रत्यागमन a + b\nअन्त\nदर्शय योग(2, 3)\n",
    "यदि अ > ५\n    दर्शय अ\nअन्त\n",
    "स्थापय सूची = [1, 2, 3]\nदर्शय लम्बाई(सूची)\n",
    "दर्शय अ\n",
]


@pytest.fixture(scope="module")
def tiny_model():
    model = BrahmaLLM.create(kind="neural", size="tiny", seed=3)
    model.fit(SMALL_CORPUS, epochs=3)
    return model


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("BRAHMA_HOME", str(tmp_path / "home"))
    return tmp_path / "home"


# ---------------------------------------------------------------------------
# tokenizer
# ---------------------------------------------------------------------------
class TestTokenizer:
    def test_aksharas_are_reversible(self):
        for text in ('दर्शय "नमस्ते, विश्व!"', "क्षत्रिय कं कि १२३ abc_def", "🕉️ सूत्र-OS"):
            assert "".join(aksharas(text)) == text

    def test_akshara_keeps_conjuncts_together(self):
        tokens = aksharas("क्षत्रिय")
        assert "क्ष" in tokens[0] + tokens[1]
        assert all(token for token in tokens)

    def test_fit_encode_decode_roundtrip(self):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        text = 'स्थापय अ = १०'
        assert tokenizer.decode(tokenizer.encode(text)) == text
        assert tokenizer.vocab_size > len(tokenizer.tokens) - len(tokenizer.tokens)  # > 0 and sane

    def test_unknown_token_maps_to_unk(self):
        tokenizer = SutraTokenizer().fit(["नमस्ते"])
        assert tokenizer.token_id("ZZZ") == tokenizer.unk_id
        assert tokenizer.unk_id == 1

    def test_special_ids_are_stable(self):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        assert (tokenizer.pad_id, tokenizer.unk_id, tokenizer.bos_id, tokenizer.eos_id) == (0, 1, 2, 3)
        assert tokenizer.encode("दर्शय", add_special=True)[0] == tokenizer.bos_id

    def test_save_load_roundtrip(self, tmp_path):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        path = str(tmp_path / "tok.json")
        tokenizer.save(path)
        loaded = SutraTokenizer.load(path)
        assert loaded.tokens == tokenizer.tokens


# ---------------------------------------------------------------------------
# n-gram model
# ---------------------------------------------------------------------------
class TestNgramModel:
    def test_probabilities_form_a_distribution(self):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        model = NgramLM(order=2, vocab_size=tokenizer.vocab_size)
        model.fit([tokenizer.encode(text, add_special=True) for text in SMALL_CORPUS])
        probs = model.next_token_probs([tokenizer.encode("दर्शय")[0]])
        assert abs(sum(probs) - 1.0) < 1e-9

    def test_training_beats_uniform(self):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        sequences = [tokenizer.encode(text, add_special=True) for text in SMALL_CORPUS]
        uniform = math.log(tokenizer.vocab_size)
        model = NgramLM(order=2, vocab_size=tokenizer.vocab_size).fit(sequences)
        assert model.loss(sequences) < uniform

    def test_save_load_roundtrip(self, tmp_path):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        model = NgramLM(order=2, vocab_size=tokenizer.vocab_size)
        model.fit([tokenizer.encode(text, add_special=True) for text in SMALL_CORPUS])
        path = str(tmp_path / "model.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(model.to_dict(), handle, ensure_ascii=False)
        with open(path, "r", encoding="utf-8") as handle:
            restored = NgramLM.from_dict(json.load(handle))
        assert restored.parameter_count() == model.parameter_count()
        assert restored.next_token_probs([1]) == pytest.approx(model.next_token_probs([1]))


# ---------------------------------------------------------------------------
# neural model
# ---------------------------------------------------------------------------
class TestNeuralModel:
    def test_gradients_match_central_differences(self):
        model = NeuralLM(vocab_size=5, d_model=3, hidden=4, order=2, seed=1)
        examples = [([1, 2], 3), ([2, 3], 4), ([0, 1], 2)]
        _loss, grads = model.loss_and_grads(examples)

        probes = [("E", 1, 0), ("W1", 2, 1), ("b1", 3, None), ("W2", 1, 2), ("b2", 2, None)]
        epsilon = 1e-5
        for name, row, column in probes:
            table = getattr(model, name)
            original = table[row] if column is None else table[row][column]

            def loss_at(delta):
                if column is None:
                    table[row] = original + delta
                else:
                    table[row][column] = original + delta
                return model.loss_and_grads(examples)[0]

            numeric = (loss_at(epsilon) - loss_at(-epsilon)) / (2 * epsilon)
            if column is None:
                table[row] = original
            else:
                table[row][column] = original
            analytic = grads[name][row] if column is None else grads[name][row][column]
            assert abs(numeric - analytic) < 1e-6, "%s की प्रवणता गलत है" % name

    def test_training_reduces_loss(self):
        tokenizer = SutraTokenizer().fit(SMALL_CORPUS)
        sequences = [tokenizer.encode(text, add_special=True) for text in SMALL_CORPUS]
        model = NeuralLM(vocab_size=tokenizer.vocab_size, d_model=8, hidden=16, order=2, seed=2)
        before = model.loss(sequences)
        model.fit(sequences, epochs=6, max_examples=200)
        assert model.epoch_losses[-1] < before

    def test_predictions_survive_save_load(self, tmp_path, tiny_model):
        directory = str(tmp_path / "ckpt")
        tiny_model.save(directory)
        restored = BrahmaLLM.load(directory)
        context = tiny_model.tokenizer.encode("दर्शय")
        assert restored.model.next_token_probs(context) == pytest.approx(
            tiny_model.model.next_token_probs(context))

    def test_same_seed_same_model(self):
        first = NeuralLM(vocab_size=6, d_model=4, hidden=5, order=2, seed=11)
        second = NeuralLM(vocab_size=6, d_model=4, hidden=5, order=2, seed=11)
        assert first.E == second.E
        assert first.W2 == second.W2


# ---------------------------------------------------------------------------
# the model's maths, executed by its own language
# ---------------------------------------------------------------------------
class TestSutraKernel:
    def test_exp_and_softmax_match_python(self):
        report = self_check(samples=3)
        assert report["exp_check"] < 1e-12
        assert report["softmax_check"] < 1e-12
        assert report["max_abs_diff"] < 1e-12

    def test_forward_pass_matches_python(self):
        model = NeuralLM(vocab_size=6, d_model=3, hidden=5, order=2, seed=4)
        result = compare(model, [1, 2])
        assert result["max_abs_diff"] < 1e-12
        assert abs(sum(result["sutra"]) - 1.0) < 1e-9

    def test_kernel_source_is_the_language(self):
        assert "कार्य" in SUTRA_MATH and "प्रत्यागमन" in SUTRA_MATH
        assert "def " not in SUTRA_MATH
        assert SutraKernel().exp(0.0) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# the OS
# ---------------------------------------------------------------------------
class TestKernel:
    def test_image_has_the_documented_layout(self):
        image = build_image()
        assert image.startswith(IMAGE_SIGNATURE)
        version, payload = unpack_image(image)
        assert version == 1 and payload

    def test_kernel_boots_and_self_tests(self):
        report = verify()
        assert report["ok"], report["problems"]
        assert report["ready"]
        assert any("स्व-परीक्षण: ठीक / ठीक" in line for line in report["output"])
        assert report["steps"] > 0

    def test_corrupt_image_is_rejected(self):
        with pytest.raises(ValueError):
            unpack_image(b"NOT-AN-IMAGE")

    def test_install_is_atomic_and_verified(self, home):
        path = install()
        assert os.path.exists(path)
        assert read_image(path) == build_image()
        assert not os.path.exists(path + ".tmp")

    def test_boot_runs_on_the_project_vm(self):
        report = boot()
        assert "🕉️ सूत्र-OS कर्नेल प्रारम्भ" in report["output"][0]


# ---------------------------------------------------------------------------
# data engine
# ---------------------------------------------------------------------------
class TestPrograms:
    def test_generator_only_emits_valid_programs(self):
        generator = ProgramGenerator(seed=9)
        programs = generator.generate("prime", count=6)
        assert programs and all(program.ok for program in programs)
        assert {program.category for program in programs} == {"अभाज्य"}

    def test_goal_selects_categories(self):
        generator = ProgramGenerator(seed=1)
        assert generator.categories_for("सूची बनाओ") == ["सूची"]
        assert generator.categories_for("") == list(generator.templates)

    def test_invalid_program_is_rejected(self):
        report = validate_program("दर्शय")
        assert not report.ok and report.error

    def test_corpus_contains_repository_programs_and_seeds(self):
        corpus = load_corpus(include_docs=False)
        assert len(corpus) >= len(SMALL_CORPUS)
        assert any("सूत्र-OS" in text for text in corpus)
        assert sutra_files(), "रिपॉज़िटरी में .sutra फ़ाइलें नहीं मिलीं"


# ---------------------------------------------------------------------------
# self-editing
# ---------------------------------------------------------------------------
class TestSelfEdit:
    def test_growth_preserves_predictions(self):
        model = NeuralLM(vocab_size=5, d_model=3, hidden=4, order=2, seed=6)
        contexts = [[1, 2], [0, 3]]
        before = [model.next_token_probs(context) for context in contexts]
        expand_hidden(model, 3)
        after = [model.next_token_probs(context) for context in contexts]
        assert model.hidden == 7
        for left, right in zip(before, after):
            assert left == pytest.approx(right, abs=1e-12)

    def test_shrink_preserves_predictions_when_columns_are_zero(self):
        model = NeuralLM(vocab_size=5, d_model=3, hidden=4, order=2, seed=6)
        contexts = [[1, 2]]
        before = model.next_token_probs(contexts[0])
        expand_hidden(model, 4)  # new columns are exactly zero
        shrink_hidden(model, 4)
        assert model.hidden == 4
        assert model.next_token_probs(contexts[0]) == pytest.approx(before, abs=1e-12)

    def test_editor_accepts_a_safe_growth_and_logs_it(self, home):
        model = NeuralLM(vocab_size=5, d_model=3, hidden=4, order=2, seed=6)
        editor = SelfEditor()
        record = editor.try_grow(model, [[1, 2], [2, 3]], extra=2)
        assert record.accepted and model.hidden == 6
        path = editor.flush()
        with open(path, "r", encoding="utf-8") as handle:
            log = json.load(handle)
        assert log and log[-1]["kind"] == "body-growth" and log[-1]["accepted"] is True

    def test_editor_installs_a_working_os(self, home):
        from brahma_llm.kernel import KERNEL_SOURCE

        editor = SelfEditor()
        record = editor.try_os(KERNEL_SOURCE)
        assert record.accepted, record.detail
        assert os.path.exists(read_image_path())

    def test_editor_rejects_a_broken_os(self, home):
        editor = SelfEditor()
        record = editor.try_os('दर्शय "बिना READY"\n')
        assert not record.accepted
        assert "READY" in record.detail


def read_image_path() -> str:
    from brahma_llm.kernel import image_path

    return image_path()


# ---------------------------------------------------------------------------
# autonomous training
# ---------------------------------------------------------------------------
class TestTrainer:
    def test_loop_trains_measures_and_keeps_the_best(self, home, tmp_path):
        from brahma_llm.trainer import AutonomousTrainer, Target

        trainer = AutonomousTrainer(workdir=str(tmp_path / "run"), seed=5, log=lambda message: None)
        report = trainer.run(Target(description="अभाज्य संख्या", keywords="prime", iterations=2,
                                    epochs=2, size="tiny", budget_seconds=120),
                             base_texts=SMALL_CORPUS)
        assert report["programs"]["generated"] == 12
        assert report["programs"]["accepted"] == 12
        assert report["programs"]["acceptance_rate"] == 1.0
        assert len(report["rounds"]) == 2
        assert report["best"]["perplexity"] <= report["rounds"][0]["holdout_perplexity"] + 1e-9
        assert os.path.isdir(report["checkpoint"])
        assert os.path.exists(report["report_path"])
        assert report["kernel"]["ok"] is True

    def test_budget_stops_the_loop(self, home, tmp_path):
        from brahma_llm.trainer import AutonomousTrainer, Target

        trainer = AutonomousTrainer(workdir=str(tmp_path / "run2"), seed=5, log=lambda message: None)
        report = trainer.run(Target(description="x", iterations=5, epochs=1, size="tiny",
                                    budget_seconds=0.0), base_texts=SMALL_CORPUS)
        assert report["rounds"] == []


# ---------------------------------------------------------------------------
# app builder
# ---------------------------------------------------------------------------
class TestAppBuilder:
    def test_slug_keeps_devanagari_and_is_safe(self):
        assert slug("प्राइम संख्या अनुप्रयोग") == "प्राइम_संख्या_अनुप्रयोग"
        assert slug("") == "app"
        assert "/" not in slug("a/b c")

    def test_builds_a_runnable_app_without_a_model(self, home, tmp_path):
        manifest = generate_app(None, "योग अनुप्रयोग", outdir=str(tmp_path / "app"))
        app_dir = manifest["dir"]
        for name in ("server.py", "index.html", "README.md", "manifest.json"):
            assert os.path.exists(os.path.join(app_dir, name))
        assert manifest["logic_runs"] is True
        assert manifest["smoke"]["ok"] is True
        assert manifest["smoke"]["status"]["engine"] == "BRAHMA"
        assert manifest["logic_origin"].startswith("fallback")

    def test_builds_with_a_trained_model(self, home, tmp_path, tiny_model):
        manifest = generate_app(tiny_model, "दर्शय अनुप्रयोग", outdir=str(tmp_path / "app2"))
        assert manifest["logic_runs"] is True
        assert manifest["smoke"]["ok"] is True
        assert manifest["model"]["params"] > 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
class TestCli:
    def test_info_reports_model_kernel_and_corpus(self, home, capsys, tiny_model):
        from brahma_llm.cli import main

        tiny_model.save(os.path.join(os.environ["BRAHMA_HOME"], "llm", "best"))
        assert main(["info", "--json"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["kernel"]["ok"] is True
        assert payload["model"]["params"] > 0

    def test_generate_and_complete(self, home, capsys, tiny_model):
        from brahma_llm.cli import main

        tiny_model.save(os.path.join(os.environ["BRAHMA_HOME"], "llm", "best"))
        assert main(["generate", "दर्शय", "--tokens", "5", "--seed", "1"]) == 0
        assert capsys.readouterr().out.strip()
        assert main(["complete", "दर्शय", "--tokens", "10", "--seed", "1"]) == 0

    def test_build_app_command(self, home, capsys, tmp_path):
        from brahma_llm.cli import main

        code = main(["build-app", "--target", "अनुप्रयोग", "--out", str(tmp_path / "cli-app"), "--json"])
        assert code == 0
        assert json.loads(capsys.readouterr().out)["smoke"]["ok"] is True

    def test_brahma_llm_subcommand_is_wired(self, home, capsys):
        from brahma.cli import main as brahma_main

        assert brahma_main(["llm", "kernel", "verify"]) == 0
        assert "READY" in capsys.readouterr().out

    def test_sutra_math_command(self, home, capsys):
        from brahma_llm.cli import main

        assert main(["sutra-math"]) == 0
        assert "त्रुटि" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# the one-command mission (target → train → self-edit → OS → app)
# ---------------------------------------------------------------------------
class TestMission:
    def test_mission_runs_the_whole_cycle(self, home, tmp_path):
        from brahma_llm.mission import run_mission

        report = run_mission("अभाज्य संख्या जाँच", outdir=str(tmp_path / "mission"),
                             iterations=1, epochs=1, size="tiny", budget=120,
                             log=lambda message: None)
        assert report["training"]["rounds"], "प्रशिक्षण चक्र नहीं चला"
        assert report["training"]["best_perplexity"] is not None
        assert report["kernel_verified"] is True
        assert report["os"]["accepted"] is True
        assert report["os"]["origin"] in ("model", "shipped-kernel")
        assert report["app"]["built"] is True
        assert report["app"]["logic_runs"] is True
        assert report["app"]["smoke_ok"] is True
        assert os.path.exists(report["report_path"])
        saved = json.load(open(report["report_path"], encoding="utf-8"))
        assert saved["target"] == "अभाज्य संख्या जाँच"

    def test_mission_without_os_or_app(self, home, tmp_path):
        from brahma_llm.mission import run_mission

        report = run_mission("सूची", outdir=str(tmp_path / "mission2"), iterations=1, epochs=1,
                             size="tiny", budget=120, write_os=False, build_app=False,
                             log=lambda message: None)
        assert report["os"]["attempted"] is False
        assert report["app"]["built"] is False
        assert report["kernel_verified"] is True

    def test_kernel_harness_boots_with_a_generated_body(self):
        from brahma_llm.kernel import build_image, verify
        from brahma_llm.mission import _compose_kernel

        source = _compose_kernel("स्थापय अ = 2 + 3\nदर्शय अ")
        report = verify(build_image(source))
        assert report["ok"], report["problems"]
        assert "5" in report["output"]

    def test_broken_generated_kernel_falls_back_to_the_shipped_one(self, home, tmp_path):
        from brahma_llm.mission import _compose_kernel
        from brahma_llm.selfedit import SelfEditor

        editor = SelfEditor(workdir=str(tmp_path / "self"))
        record = editor.try_os(_compose_kernel("स्थापय अ = "))
        assert record.accepted is False
        assert "SyntaxError" in record.detail or "ParseError" in record.detail or "LexError" in record.detail
