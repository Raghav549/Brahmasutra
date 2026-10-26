"""🕉️ स्वायत्त प्रशिक्षक — set a target, then let ब्रह्म train itself.

The loop is deliberately boring and measurable, which is what makes it
trustworthy:

1. **Generate** candidate सूत्र programs aimed at the target
   (:class:`brahma_llm.programs.ProgramGenerator`).
2. **Filter** them by *executing* each one; failures never reach the corpus.
3. **Train** — cold start on the first round, warm start afterwards, on the
   repository corpus plus the accepted programs.  The held-out split is taken
   from real repository files only, so a model cannot cheat by memorising its
   own generations.
4. **Measure** held-out perplexity.
5. **Keep** the checkpoint if it is the best so far, otherwise keep the old one.
6. **Edit its own body** (grow the hidden layer, prediction-preserving) when the
   last round improved — capacity only grows for a reason.
7. **Stop** on the target threshold, on ``patience`` rounds without
   improvement, on the iteration cap, or when the time budget is spent.

Every number in the report is produced by this loop; ``report.json`` is written
next to the checkpoint so the run can be reproduced with the same seed.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from .model import BrahmaLLM
from .programs import ProgramGenerator, load_corpus, sutra_files
from .selfedit import SelfEditor


@dataclass
class Target:
    """What the user wants, and the budget they are willing to spend."""

    description: str = "सूत्र में वैध कार्यक्रम लिखना सीखो"
    keywords: str = ""
    iterations: int = 3
    programs_per_iteration: int = 6
    epochs: int = 3
    budget_seconds: float = 180.0
    threshold: Optional[float] = None
    patience: int = 2
    size: str = "tiny"
    kind: str = "neural"
    allow_growth: bool = True

    def as_dict(self) -> dict:
        return {
            "description": self.description,
            "keywords": self.keywords,
            "iterations": self.iterations,
            "programs_per_iteration": self.programs_per_iteration,
            "epochs": self.epochs,
            "budget_seconds": self.budget_seconds,
            "threshold": self.threshold,
            "patience": self.patience,
            "size": self.size,
            "kind": self.kind,
            "allow_growth": self.allow_growth,
        }


def split_corpus(texts: Sequence[str], holdout_every: int = 5) -> tuple:
    """Deterministic train/hold-out split from real repository files."""
    holdout = [text for index, text in enumerate(texts) if index % holdout_every == 0]
    train = [text for index, text in enumerate(texts) if index % holdout_every != 0]
    return train or list(texts), holdout or list(texts)


class AutonomousTrainer:
    """The self-training loop described in this module's docstring."""

    def __init__(self, workdir: Optional[str] = None, seed: int = 7, log=None, editor: Optional[SelfEditor] = None):
        from brahma_paths import data_root

        self.workdir = workdir or data_root("llm", create=True)
        self.seed = seed
        self.log = log or (lambda message: print(message))
        if editor is None:
            editor = SelfEditor(workdir=os.path.join(self.workdir, "self"), log=self.log)
        self.editor = editor
        self.generator = ProgramGenerator(seed=seed)

    # -- helpers ---------------------------------------------------------
    def _elapsed(self, started: float) -> float:
        return time.time() - started

    def _save(self, model: BrahmaLLM, name: str) -> str:
        return model.save(os.path.join(self.workdir, name))

    # -- main loop -------------------------------------------------------
    def run(self, target: Optional[Target] = None, base_texts: Optional[Sequence[str]] = None) -> dict:
        target = target or Target()
        started = time.time()

        base = list(base_texts) if base_texts is not None else load_corpus(include_docs=False)
        train_texts, holdout_texts = split_corpus(base)
        holdout_texts = holdout_texts[:12]

        self.log("🕉️ लक्ष्य: %s" % target.description)
        self.log("   आधार: %d पाठ, परीक्षा: %d पाठ, बजट: %.0f सेकंड"
                 % (len(train_texts), len(holdout_texts), target.budget_seconds))

        model = BrahmaLLM.create(kind=target.kind, size=target.size, seed=self.seed)
        best: Dict[str, object] = {"perplexity": float("inf"), "iteration": 0, "path": ""}
        rounds: List[dict] = []
        generated_total = 0
        passed_total = 0
        stale = 0

        for iteration in range(1, target.iterations + 1):
            if self._elapsed(started) > target.budget_seconds:
                self.log("  ⏱️ बजट समाप्त — चक्र रोका गया")
                break

            # 1-2. generate and filter candidates
            candidates = self.generator.generate(
                target.keywords or target.description,
                count=target.programs_per_iteration,
            )
            accepted = [candidate for candidate in candidates if candidate.ok]
            generated_total += len(candidates)
            passed_total += len(accepted)
            self.log("  चक्र %d: %d/%d कार्यक्रम वैध" % (iteration, len(accepted), len(candidates)))

            # 3. train
            train_this_round = list(train_texts) + [candidate.source for candidate in accepted]
            if iteration == 1:
                model.fit(train_this_round, epochs=target.epochs,
                          on_epoch=lambda epoch, loss: self.log("    epoch %d loss %.4f" % (epoch + 1, loss)))
            else:
                # Anneal: successive rounds take smaller steps so that warm
                # starts refine the model instead of oscillating around a
                # minimum (measured — see docs/LLM.md).
                current = getattr(model.model, "learning_rate", 0.02)
                model.continue_training(train_this_round, epochs=max(1, target.epochs - 1),
                                        learning_rate=max(0.004, current * 0.6))

            # 4. measure
            metrics = model.evaluate(holdout_texts)
            elapsed = self._elapsed(started)
            improved = metrics["perplexity"] < best["perplexity"]
            self.log("    held-out perplexity %.3f (%s)" % (metrics["perplexity"], "सुधरा" if improved else "नहीं"))

            # 5. keep the winner
            if improved:
                best = {"perplexity": metrics["perplexity"], "iteration": iteration, "path": self._save(model, "best")}
                stale = 0
            else:
                stale += 1
                if best["path"]:
                    model = BrahmaLLM.load(str(best["path"]))

            # 6. self-edit: capacity may grow after a win
            body_edit = None
            if target.allow_growth and improved and getattr(model.model, "kind", "") == "neural":
                contexts = [model.tokenizer.encode(text)[:4] for text in holdout_texts[:5]]
                context_ids = [ctx for ctx in contexts if ctx]
                if context_ids:
                    body_edit = self.editor.try_grow(model.model, context_ids, extra=4).as_dict()
                    best["path"] = self._save(model, "best")

            rounds.append({
                "iteration": iteration,
                "programs_generated": len(candidates),
                "programs_accepted": len(accepted),
                "categories": sorted({candidate.category for candidate in candidates}),
                "holdout_perplexity": metrics["perplexity"],
                "holdout_tokens": metrics["tokens"],
                "train_texts": len(train_this_round),
                "params": model.model.parameter_count(),
                "improved": improved,
                "elapsed": round(elapsed, 2),
                "body_edit": body_edit,
            })

            # 7. stopping rules
            if target.threshold is not None and metrics["perplexity"] <= target.threshold:
                self.log("  🎯 लक्ष्य सीमा पूरी हुई")
                break
            if stale >= target.patience:
                self.log("  ⏸️ %d चक्र बिना सुधार — रोका गया" % stale)
                break

        # final checkpoint + report
        final_metrics = model.evaluate(holdout_texts)
        if final_metrics["perplexity"] < best["perplexity"]:
            best = {"perplexity": final_metrics["perplexity"], "iteration": len(rounds),
                    "path": self._save(model, "best")}

        from .kernel import verify as verify_kernel

        kernel = verify_kernel()
        report = {
            "target": target.as_dict(),
            "seed": self.seed,
            "started": started,
            "elapsed": round(self._elapsed(started), 2),
            "rounds": rounds,
            "best": {"perplexity": best["perplexity"], "iteration": best["iteration"], "path": best["path"]},
            "final": {"perplexity": final_metrics["perplexity"], "loss": final_metrics["loss"]},
            "params": model.model.parameter_count(),
            "vocab_size": model.tokenizer.vocab_size,
            "programs": {"generated": generated_total, "accepted": passed_total,
                         "acceptance_rate": (passed_total / generated_total) if generated_total else 0.0},
            "kernel": {"ok": kernel["ok"], "steps": kernel["steps"], "image_bytes": kernel["image_bytes"]},
            "self_edits": [record.as_dict() for record in self.editor.records],
            "corpus_files": len(sutra_files()),
        }
        report_path = os.path.join(self.workdir, "report.json")
        os.makedirs(self.workdir, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=1)
        self.editor.flush()
        report["report_path"] = report_path
        report["checkpoint"] = best["path"]
        self.log("  🏁 सर्वोत्तम perplexity %.3f — %s" % (best["perplexity"], best["path"]))
        return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="स्वायत्त प्रशिक्षण")
    parser.add_argument("--target", default="सूत्र में वैध कार्यक्रम लिखना सीखो")
    parser.add_argument("--keywords", default="")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--size", default="tiny", choices=sorted(["tiny", "small", "medium", "large"]))
    parser.add_argument("--kind", default="neural", choices=("neural", "ngram"))
    parser.add_argument("--budget", type=float, default=180.0, help="सेकंड")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--workdir", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    target = Target(description=args.target, keywords=args.keywords, iterations=args.iterations,
                    epochs=args.epochs, size=args.size, kind=args.kind, budget_seconds=args.budget,
                    threshold=args.threshold)
    trainer = AutonomousTrainer(workdir=args.workdir, log=(lambda message: None) if args.json else print)
    report = trainer.run(target)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        print("रिपोर्ट: %s" % report["report_path"])
    return 0 if report["programs"]["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
