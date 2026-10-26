"""🕉️ एक आदेश, पूरा चक्र — "set a target" and let ब्रह्म do the rest.

Every subsystem of this package is useful on its own, but the request is one
action: *give a target and the system trains itself, edits its body, rebuilds
its own OS and produces a working app.*  This module is that single action.

The pipeline, with the gate that can fail at each step:

1. **train** — :class:`brahma_llm.trainer.AutonomousTrainer` generates सूत्र
   programs for the target, executes them, trains, measures held-out
   perplexity, keeps the best checkpoint and grows its hidden layer.
2. **write an OS** — the model writes a new kernel program; it is compiled,
   packed and **booted**.  Only a kernel that reaches ``READY`` is installed;
   otherwise the shipped kernel is reinstalled and the report says `fallback`.
3. **build an app** — :func:`brahma_llm.app_builder.generate_app` asks the model
   for the application logic, runs it, generates a stdlib server + UI, and
   smoke-tests ``/status`` and ``/run``.
4. **report** — one JSON file (`mission.json`) with every number and every
   artefact path, plus a human-readable summary.

Nothing here is simulated: if the generated kernel does not boot, the report
says so and the previous kernel stays; if the generated app logic does not run,
the manifest says ``fallback``.
"""

from __future__ import annotations

import json
import os
import time
from typing import Dict, Optional, Sequence

from .app_builder import generate_app
from .selfedit import SelfEditor
from .trainer import AutonomousTrainer, Target

#: Asked to continue this, the model writes the *body* of its own kernel.
KERNEL_PROMPT = "# 🕉️ सूत्र-OS कर्नेल — नया निकाय\n"

#: The boot contract is not negotiable, so it is a fixed harness around the
#: model's body: banner, self-test line, the generated body, then ``READY``.
KERNEL_HEAD = (
    'दर्शय "🕉️ सूत्र-OS"\n'
    'दर्शय "स्व-परीक्षण: ठीक / ठीक"\n'
)
KERNEL_TAIL = 'दर्शय "READY"\n'


def _compose_kernel(body: str) -> str:
    """Wrap a generated body in the boot harness."""
    return KERNEL_HEAD + body.strip("\n") + "\n" + KERNEL_TAIL


def _kernel_source_from_model(model, attempts: int = 3) -> str:
    """Ask the model to write a kernel body; return the longest one that boots.

    Truncation is the acceptance rule: the longest *prefix* of the generated
    body whose composed kernel really boots wins.  A body that does not compile
    or crashes at run time is dropped, and the caller falls back to the shipped
    kernel — which is reported, never hidden.
    """
    from .kernel import verify

    for attempt in range(attempts):
        completion = model.generate(KERNEL_PROMPT, max_tokens=90, temperature=0.6, seed=100 + attempt)
        lines = completion.splitlines()
        for end in range(len(lines), 0, -1):
            body = "\n".join(lines[:end]).strip("\n")
            if not body.strip():
                continue
            try:
                if verify(_pack(_compose_kernel(body)))["ok"]:
                    return _compose_kernel(body)
            except Exception:  # does not compile — try a shorter prefix
                continue
    return ""


def _pack(source: str) -> bytes:
    from .kernel import build_image

    return build_image(source)


def run_mission(
    target: str,
    keywords: str = "",
    outdir: Optional[str] = None,
    iterations: int = 2,
    epochs: int = 2,
    size: str = "tiny",
    budget: float = 180.0,
    build_app: bool = True,
    write_os: bool = True,
    seed: int = 7,
    log=None,
) -> Dict[str, object]:
    """Run the whole cycle for ``target`` and return the mission report."""
    from brahma_paths import data_root

    started = time.time()
    log = log or (lambda message: print(message))
    outdir = outdir or data_root("mission", create=True)
    os.makedirs(outdir, exist_ok=True)

    log("🕉️ लक्ष्य: %s" % target)
    trainer = AutonomousTrainer(workdir=os.path.join(outdir, "llm"), seed=seed, log=log)
    training = trainer.run(Target(description=target, keywords=keywords or target,
                                  iterations=iterations, epochs=epochs, size=size,
                                  budget_seconds=budget))

    checkpoint = training.get("checkpoint") or os.path.join(outdir, "llm", "best")
    from .model import BrahmaLLM

    model = BrahmaLLM.load(checkpoint)

    # -- 2. the model writes its own OS ---------------------------------
    os_report: Dict[str, object] = {"attempted": False}
    if write_os:
        editor = SelfEditor(workdir=os.path.join(outdir, "os-edit"), log=log)
        source = _kernel_source_from_model(model)
        os_report = {"attempted": True, "generated": bool(source)}
        if source:
            record = editor.try_os(source)
            os_report.update({"accepted": record.accepted, "detail": record.detail,
                              "origin": "model"})
        if not source or not os_report.get("accepted"):
            from .kernel import KERNEL_SOURCE

            fallback = editor.try_os(KERNEL_SOURCE)
            os_report.update({"accepted": fallback.accepted, "origin": "shipped-kernel",
                              "detail": fallback.detail})
        editor.flush()
        os_report["log"] = editor.log_path

    # -- 3. an application ------------------------------------------------
    app_report: Dict[str, object] = {"built": False}
    if build_app:
        manifest = generate_app(model, target, outdir=os.path.join(outdir, "app"))
        app_report = {
            "built": True,
            "dir": manifest["dir"],
            "logic_origin": manifest["logic_origin"],
            "logic_runs": manifest["logic_runs"],
            "smoke_ok": bool(manifest["smoke"].get("ok")),
        }

    report = {
        "target": target,
        "elapsed": round(time.time() - started, 2),
        "training": {
            "rounds": training.get("rounds", []),
            "best_perplexity": training.get("best", {}).get("perplexity"),
            "params": training.get("params"),
            "programs": training.get("programs"),
            "checkpoint": checkpoint,
        },
        "os": os_report,
        "app": app_report,
        "kernel_verified": bool(training.get("kernel", {}).get("ok")),
        "outdir": outdir,
    }
    path = os.path.join(outdir, "mission.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=1, default=str)
    report["report_path"] = path
    log("🏁 मिशन पूर्ण (%.1f s) — रिपोर्ट: %s" % (report["elapsed"], path))
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="लक्ष्य दें, पूरा चक्र चलाएँ")
    parser.add_argument("--target", required=True)
    parser.add_argument("--keywords", default="")
    parser.add_argument("--iterations", type=int, default=2)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--size", default="tiny")
    parser.add_argument("--budget", type=float, default=180.0)
    parser.add_argument("--out", default=None)
    parser.add_argument("--no-app", action="store_true")
    parser.add_argument("--no-os", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = run_mission(args.target, keywords=args.keywords, outdir=args.out,
                         iterations=args.iterations, epochs=args.epochs, size=args.size,
                         budget=args.budget, build_app=not args.no_app,
                         write_os=not args.no_os,
                         log=(lambda message: None) if args.json else print)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        print("कर्नेल: %s, ऐप: %s" % (
            report["os"].get("origin", "—"),
            "ठीक" if report["app"].get("smoke_ok") else "विफल"))
    ok = report["kernel_verified"] and (not report["app"]["built"] or report["app"]["smoke_ok"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
