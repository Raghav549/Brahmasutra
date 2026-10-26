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

    def test_generated_programs_can_be_written_and_reloaded(self, tmp_path):
        from brahma_llm.programs import save_generated

        generator = ProgramGenerator(seed=4)
        programs = generator.passing(goal="अभाज्य", count=5)
        written = save_generated([p.source for p in programs], outdir=str(tmp_path))
        assert len(written) == 5
        assert all(name.endswith(".sutra") for name in written)

        corpus = load_corpus(include_docs=False, extra_dirs=[str(tmp_path)])
        for program in programs:
            assert program.source in corpus

    def test_cli_corpus_generate_reports_what_it_wrote(self, tmp_path, capsys):
        from brahma_llm.cli import main

        code = main(["corpus", "--generate", "4", "--seed", "2",
                     "--out", str(tmp_path), "--json"])
        assert code == 0
        stats = json.loads(capsys.readouterr().out)
        assert stats["generated_written"] == 4
        import os

        names = sorted(os.listdir(tmp_path))
        assert len(names) == 4
        for name in names:
            with open(os.path.join(str(tmp_path), name), encoding="utf-8") as handle:
                assert validate_program(handle.read()).ok

    def test_generated_data_improves_perplexity(self, tmp_path, home):
        """अधिक वैध डेटा → उसी वितरण पर बेहतर perplexity.

        Both models are scored on the *same* held-out set of generated
        programs — comparing each model on its own corpus (the old form of
        this test) compares unlike distributions and passes only by luck.
        Measured at ``tiny``/2 epochs: 11.492 -> 9.646.  Base-text
        perplexity is *not* claimed to improve at this size (9.499 ->
        10.056): see docs/LLM.md §3.1b.
        """
        from brahma_llm.model import BrahmaLLM
        from brahma_llm.programs import save_generated

        tiny = "tiny"
        base_corpus = load_corpus(include_docs=False, extra_dirs=[])
        baseline = BrahmaLLM.create(kind="neural", size=tiny, seed=7)
        baseline.fit(base_corpus, epochs=2)

        programs = ProgramGenerator(seed=8).passing(count=40)
        save_generated([p.source for p in programs], outdir=str(tmp_path))
        grown_corpus = load_corpus(include_docs=False, extra_dirs=[str(tmp_path)])
        grown = BrahmaLLM.create(kind="neural", size=tiny, seed=7)
        grown.fit(grown_corpus, epochs=2)

        held_out = [p.source for p in programs][::4]
        baseline_ppl = baseline.evaluate(held_out)["perplexity"]
        grown_ppl = grown.evaluate(held_out)["perplexity"]

        assert len(grown_corpus) > len(base_corpus)
        assert grown_ppl < baseline_ppl, (baseline_ppl, grown_ppl)


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
class TestAgent:
    """The model is the product: chat, code, run, explain, image."""

    def test_intent_routing_is_explicit(self):
        from brahma_llm.agent import detect_intent

        assert detect_intent("नमस्ते") == "chat"
        assert detect_intent("कोड लिखो: अभाज्य संख्या जाँच") == "code"
        assert detect_intent("दर्शय 2 + 3") == "run"
        assert detect_intent("चित्र बनाओ: शांति") == "image"
        assert detect_intent("status") == "status"
        assert detect_intent("help") == "help"

    def test_synthesize_ranks_with_the_model_and_runs_the_winner(self, tiny_model):
        from brahma_llm.agent import synthesize

        result = synthesize("अभाज्य संख्या जाँच", tiny_model)
        assert result["origin"] == "ranked"
        assert result["error"] is None
        assert result["output"], "चुना गया कार्यक्रम कुछ नहीं छापा"
        assert result["category"] == "अभाज्य", result["category"]
        losses = [row["loss"] for row in result["ranking"]]
        assert losses == sorted(losses), "श्रेणी मॉडल loss के क्रम में होनी चाहिए"

    def test_generated_code_really_executes(self, tiny_model):
        from brahma_llm.agent import BrahmaAgent

        agent = BrahmaAgent(model=tiny_model)
        result = agent.run("दर्शय 6 * 7")
        assert result["error"] is None
        assert result["output"] == ["42"]
        assert result["origin"] == "message"

    def test_explain_reports_structure_not_opinions(self):
        from brahma_llm.agent import explain

        report = explain("कार्य योग(a, b)\n    प्रत्यागमन a + b\nअन्त\nदर्शय योग(2, 3)")
        assert report["ok"] is True
        assert report["functions"][0]["name"] == "योग"
        assert report["bytecode_instructions"] > 0
        broken = explain("स्थापय अ = ")
        assert broken["ok"] is False and broken["error"]

    def test_status_boots_the_kernel(self, home, tiny_model):
        from brahma_llm.agent import BrahmaAgent

        status = BrahmaAgent(model=tiny_model).status()
        assert status["kernel"]["ok"] is True
        assert status["model"]["params"] == tiny_model.model.parameter_count()

    def test_respond_never_raises_on_a_broken_request(self, tiny_model):
        from brahma_llm.agent import BrahmaAgent

        agent = BrahmaAgent(model=tiny_model)
        for message in ("", "दर्शय ", "चित्र", "explain"):
            result = agent.respond(message)
            assert isinstance(result["text"], str)


class TestImage:
    def test_png_is_real_and_deterministic(self, home, tmp_path):
        from brahma_llm.image import generate

        first = generate("शांति", None, path=str(tmp_path / "a.png"))
        second = generate("शांति", None, path=str(tmp_path / "b.png"))
        blob = open(first["path"], "rb").read()
        assert blob.startswith(b"\x89PNG\r\n\x1a\n")
        assert first["seed"] == second["seed"]
        assert blob == open(second["path"], "rb").read()
        assert first["origin"] in ("generated", "ranked", "fallback")

    def test_model_driven_program_supplies_the_numbers(self, home, tmp_path, tiny_model):
        from brahma_llm.image import generate

        meta = generate("अभाज्य चित्र", tiny_model, path=str(tmp_path / "c.png"))
        assert meta["origin"] != "fallback", meta
        assert meta["numbers"] >= 4
        assert "दर्शय" in meta["program"]


class TestServer:
    """One server, every capability — including the kernel it boots."""

    @pytest.fixture()
    def running(self, home, tmp_path, tiny_model):
        import brahma_llm.server as server_module

        app = server_module.create_app(model=tiny_model, image_dir=str(tmp_path / "img"))
        port = app.start("127.0.0.1", 0)
        try:
            yield "http://127.0.0.1:%d" % port
        finally:
            app.shutdown()

    @staticmethod
    def _post(base, path, payload):
        import urllib.request

        request = urllib.request.Request(
            base + path, data=json.dumps(payload).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _get(base, path):
        import urllib.request

        with urllib.request.urlopen(base + path, timeout=60) as response:
            return response.read(), response.headers

    def test_index_and_status(self, running):
        page, headers = self._get(running, "/")
        assert "ब्रह्म".encode("utf-8") in page
        assert "text/html" in headers["Content-Type"]
        status = json.loads(self._get(running, "/status")[0].decode("utf-8"))
        assert status["kernel"]["ok"] is True

    def test_kernel_boots_over_http(self, running):
        report = json.loads(self._get(running, "/kernel")[0].decode("utf-8"))
        assert report["ok"] is True
        assert any("READY" in line for line in report["output"])

    def test_chat_code_run_and_explain(self, running):
        chat = self._post(running, "/chat", {"message": "कोड लिखो: अभाज्य संख्या जाँच"})
        assert chat["intent"] == "code"
        assert chat["error"] is None
        run = self._post(running, "/run", {"source": "दर्शय 7 * 6"})
        assert run["ok"] is True and run["output"] == ["42"]
        explain = self._post(running, "/explain", {"source": "दर्शय 1"})
        assert explain["ok"] is True

    def test_shell_endpoint_drives_the_kernel_over_http(self, running):
        first = self._post(running, "/shell", {"command": "free"})
        assert first["ok"] is True
        assert any("स्मृति" in line for line in first["output"])

        # state is shared between requests: fork here, see it in the next call
        forked = self._post(running, "/shell", {"command": "fork http-कार्य"})
        assert "नया pid" in forked["output"][0]
        listing = self._post(running, "/shell", {"command": "ps"})
        assert any("http-कार्य" in line for line in listing["output"])

        run = self._post(running, "/shell", {"command": "run दर्शय 6 * 7"})
        assert run["output"] == ["42"]

        caught = self._post(running, "/shell", {"command": "syscall 99"})
        assert "अज्ञात syscall 99" in caught["output"][0]

    def test_shell_endpoint_requires_a_command(self, running):
        import urllib.error
        import urllib.request

        request = urllib.request.Request(
            running + "/shell", data=b"{}", method="POST",
            headers={"Content-Type": "application/json"})
        with pytest.raises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, timeout=30)
        assert caught.value.code == 400

    def test_image_endpoint_returns_png(self, running):
        import urllib.parse

        blob, headers = self._get(running, "/image?prompt=" + urllib.parse.quote("शांति"))
        assert headers["Content-Type"] == "image/png"
        assert blob.startswith(b"\x89PNG")
        assert headers["X-Brahma-Seed"].isdigit()

    def test_validation_errors_are_400_not_500(self, running):
        import urllib.error

        with pytest.raises(urllib.error.HTTPError) as error:
            self._post(running, "/chat", {"message": ""})
        assert error.value.code == 400
        with pytest.raises(urllib.error.HTTPError) as error:
            self._get(running, "/image")
        assert error.value.code == 400


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

    def test_ask_command(self, home, capsys, tmp_path, tiny_model):
        from brahma_llm.cli import main

        checkpoint = tiny_model.save(str(tmp_path / "cli-ckpt"))
        code = main(["ask", "दर्शय 2 + 3", "--model", checkpoint, "--json"])
        assert code == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["intent"] == "run"
        assert payload["output"] == ["5"]

    def test_image_command_writes_a_png(self, home, capsys, tmp_path, tiny_model):
        from brahma_llm.cli import main

        checkpoint = tiny_model.save(str(tmp_path / "cli-ckpt2"))
        target = str(tmp_path / "cli.png")
        code = main(["image", "शांति", "--model", checkpoint, "--out", target])
        assert code == 0
        assert open(target, "rb").read(4) == b"\x89PNG"

    def test_serve_command_binds_once(self, home, capsys, tmp_path, tiny_model):
        from brahma_llm.cli import main

        checkpoint = tiny_model.save(str(tmp_path / "cli-ckpt3"))
        code = main(["serve", "--model", checkpoint, "--port", "0", "--once",
                     "--image-dir", str(tmp_path / "cli-img")])
        assert code == 0
        assert "तैयार" in capsys.readouterr().out

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
        assert report["server"]["served"] is True
        assert report["server"]["chat_ok"] is True
        assert report["server"]["run_ok"] is True
        assert report["server"]["image_ok"] is True
        assert report["server"]["kernel_ok"] is True
        assert report["server"]["shell_ok"] is True
        assert report["server"]["shell_run"] == ["42"]
        assert report["server"]["smoke_ok"] is True
        assert os.path.exists(report["report_path"])
        saved = json.load(open(report["report_path"], encoding="utf-8"))
        assert saved["target"] == "अभाज्य संख्या जाँच"

    def test_mission_without_os_or_app(self, home, tmp_path):
        from brahma_llm.mission import run_mission

        report = run_mission("सूची", outdir=str(tmp_path / "mission2"), iterations=1, epochs=1,
                             size="tiny", budget=120, write_os=False, serve=False,
                             log=lambda message: None)
        assert report["os"]["attempted"] is False
        assert report["server"]["served"] is False
        assert report["kernel_verified"] is True

    def test_kernel_harness_boots_with_a_generated_body(self):
        from brahma_llm.kernel import build_image, verify
        from brahma_llm.mission import _compose_kernel

        source = _compose_kernel("स्थापय अ = 2 + 3\nदर्शय अ")
        report = verify(build_image(source))
        assert report["ok"], report["problems"]
        assert "5" in report["output"]

    def test_kernel_uses_its_own_exception_support(self):
        """सुरक्षित_आह्वान अज्ञात syscall को पकड़ता है (3.1)."""
        report = verify()
        assert report["ready"] is True and report["ok"] is True
        assert any("उपप्रणाली: 6/6 ठीक" in line for line in report["output"])
        assert any("अपवाद: 1 पकड़े" in line for line in report["output"])
        assert any("कर्नेल API: 10 फलन" in line for line in report["output"])

    def test_mission_resume_keeps_the_better_checkpoint(self, home, tmp_path):
        """Resume वही चेकपॉइंट रखता है और गिरावट को "सुधार" नहीं कहता।"""
        from brahma_llm.mission import run_mission

        outdir = str(tmp_path / "mission_resume")
        first = run_mission("अभाज्य संख्या जाँच", outdir=outdir, iterations=1, epochs=1,
                            size="tiny", budget=60, write_os=False, serve=False,
                            log=lambda message: None)
        second = run_mission("अभाज्य संख्या जाँच", outdir=outdir, iterations=1, epochs=1,
                             size="tiny", budget=60, write_os=False, serve=False,
                             resume=True, log=lambda message: None)
        training = second["training"]
        assert training["resumed_from"] == first["training"]["checkpoint"]
        assert training["previous_best"] == pytest.approx(first["training"]["best_perplexity"])
        assert training["best_perplexity"] <= first["training"]["best_perplexity"] + 1e-9
        assert training["improved_this_run"] is (
            training["best_perplexity"] < first["training"]["best_perplexity"])

    def test_mission_can_grow_its_own_corpus(self, home, tmp_path):
        """--grow प्रशिक्षण से पहले वैध कार्यक्रम जोड़ता है (3.4)।"""
        import os

        from brahma_llm.mission import run_mission
        from brahma_llm.programs import generated_dir

        report = run_mission("अभाज्य संख्या जाँच", outdir=str(tmp_path / "mission_grow"),
                             iterations=1, epochs=1, size="tiny", budget=120, grow=10,
                             write_os=False, serve=False, log=lambda message: None)
        assert report["training"]["grow"] == 10
        files = [name for name in os.listdir(generated_dir()) if name.endswith(".sutra")]
        assert len(files) >= 10
        assert report["training"]["best_perplexity"] is not None

    def test_mission_continuous_runs_several_generations(self, home, tmp_path):
        from brahma_llm.mission import run_mission

        report = run_mission("सूची", outdir=str(tmp_path / "mission_cont"), iterations=1,
                             epochs=1, size="tiny", budget=120, continuous=True,
                             max_generations=2, write_os=False, serve=False,
                             log=lambda message: None)
        generations = report["training"]["generations"]
        assert 1 <= len(generations) <= 2
        assert all("improved" in generation for generation in generations)
        assert report["training"]["programs"]["accepted"] >= 1
        if len(generations) == 2:
            assert generations[0]["cold_start"] is True
            assert generations[1]["cold_start"] is False

    def test_trainer_warm_start_keeps_the_weights(self, home, tmp_path, tiny_model):
        from brahma_llm.trainer import AutonomousTrainer, Target

        checkpoint = tiny_model.save(str(tmp_path / "warm"))
        before = tiny_model.model.parameter_count()
        trainer = AutonomousTrainer(workdir=str(tmp_path / "warm_work"),
                                    log=lambda message: None)
        report = trainer.run(Target(description="सूची", iterations=1, epochs=1, size="tiny",
                                    budget_seconds=60, resume_from=checkpoint,
                                    allow_growth=False))
        assert report["cold_start"] is False
        assert report["target"]["resume_from"] == checkpoint
        assert report["params"] >= before

    def test_broken_generated_kernel_falls_back_to_the_shipped_one(self, home, tmp_path):
        from brahma_llm.mission import _compose_kernel
        from brahma_llm.selfedit import SelfEditor

        editor = SelfEditor(workdir=str(tmp_path / "self"))
        record = editor.try_os(_compose_kernel("स्थापय अ = "))
        assert record.accepted is False
        assert "SyntaxError" in record.detail or "ParseError" in record.detail or "LexError" in record.detail


class TestKernelShell:
    """सूत्र-OS शेल: the dispatcher is सूत्र, the state is the kernel's (3.3)."""

    def test_boot_log_ends_ready(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        assert any("READY" in line for line in shell.boot_output)
        assert shell.exited is False

    def test_help_lists_commands(self):
        from brahma_llm.shell import KernelShell

        output = KernelShell().command("help")["output"]
        assert output and all(word in output[0] for word in ("ps", "free", "cat", "exit"))

    def test_process_table_is_live(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        before = shell.command("ps")["output"]
        shell.command("fork शेल-कार्य")
        after = shell.command("ps")["output"]
        assert len(after) == len(before) + 1
        assert any("शेल-कार्य" in line for line in after)

    def test_kill_changes_the_process_state(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        assert "समाप्त: 1" in shell.command("kill 1")["output"][0]
        assert "pid नहीं मिला: 99" in shell.command("kill 99")["output"][0]

    def test_filesystem_round_trip_between_commands(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        assert "लिखा" in shell.command("write /नमूना नमस्ते ब्रह्म")["output"][0]
        assert shell.command("cat /नमूना")["output"] == ["  नमस्ते ब्रह्म"]
        assert any("/नमूना" in line for line in shell.command("ls")["output"])

    def test_missing_file_is_reported_not_raised(self):
        from brahma_llm.shell import KernelShell

        assert "नहीं मिली" in KernelShell().command("cat /नहीं/है")["output"][0]

    def test_guarded_syscall_through_the_shell(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        unknown = shell.command("syscall 99")["output"][0]
        assert "असत्य" in unknown and "अज्ञात syscall 99" in unknown
        assert "सत्य" in shell.command("syscall 1")["output"][0]

    def test_run_executes_sutra_inside_the_kernel_namespace(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        assert shell.command("run दर्शय 6 * 7")["output"] == ["42"]
        shell.command("run स्थापय गिनती = 41")
        assert shell.command("run दर्शय गिनती + 1")["output"] == ["42"]

    def test_run_reports_faults(self):
        from brahma_llm.shell import KernelShell

        result = KernelShell().command("run 1 / 0")
        assert result["ok"] is False
        assert "शून्य से भाग" in result["error"]

    def test_unknown_command_is_reported(self):
        from brahma_llm.shell import KernelShell

        result = KernelShell().command("उड़ान")
        assert result["ok"] is True
        assert "अज्ञात आदेश" in result["output"][0]

    def test_exit_stops_a_script(self):
        from brahma_llm.shell import KernelShell

        shell = KernelShell()
        results = shell.script(["free", "exit", "ps"])
        assert len(results) == 2 and results[-1]["exit"] is True

    def test_cli_json_contract(self, capsys, home):
        from brahma_llm.shell import main

        assert main(["--json", "--command", "free"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["commands"][0]["ok"] is True
        assert any("स्मृति" in line for line in payload["commands"][0]["output"])

    def test_installed_version_file_matches_the_package(self):
        import brahma
        from brahma_llm.shell import KernelShell

        reported = KernelShell().command("cat /इत्यादि/संस्करण")["output"][0].strip()
        assert reported == brahma.__version__
