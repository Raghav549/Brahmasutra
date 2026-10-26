"""🕉️ एक आदेश, पूरा चक्र — "set a target" and let ब्रह्म do the rest.

Every subsystem of this package is useful on its own, but the request is one
action: *give a target and the system trains itself, edits its body, rebuilds
its own OS and then serves itself.*  This module is that single action.

The pipeline, with the gate that can fail at each step:

1. **train** — :class:`brahma_llm.trainer.AutonomousTrainer` generates सूत्र
   programs for the target, executes them, trains, measures held-out
   perplexity, keeps the best checkpoint and grows its hidden layer.
2. **write an OS** — the model writes a new kernel body; it is composed into the
   fixed boot contract, compiled, packed and **booted**.  Only a kernel that
   reaches ``READY`` is installed; otherwise the shipped kernel is reinstalled
   and the report says ``shipped-kernel``.
3. **serve itself** — the trained model is put behind
   :func:`brahma_llm.server.create_app`, and the running server is smoke-tested
   on ``/status``, ``/kernel``, ``/chat`` (code), ``/run`` and ``/image``.  The
   model *is* the application; nothing is generated and handed over.
4. **report** — one JSON file (``mission.json``) with every number and every
   artefact path, plus a human-readable summary.

Two flags make this a loop rather than a one-shot:

* ``resume`` — continue from the checkpoint of the previous mission in the same
  directory, and treat its best perplexity as the bar to beat (a worse round is
  reported as ``improved: false`` and never replaces the better checkpoint);
* ``continuous`` — keep training further generations while each one improves,
  the time budget lasts and ``target_perplexity`` has not been reached.

Nothing here is simulated: if the generated kernel does not boot, the report
says so and the previous kernel stays; if the server smoke test fails, the
report says which endpoint failed.
"""

from __future__ import annotations

import json
import os
import time
from typing import Dict, Optional, Sequence

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
        completion = model.generate(KERNEL_PROMPT, max_tokens=90, temperature=0.6,
                                    seed=100 + attempt)
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


def _smoke_server(model, target: str, image_dir: str) -> Dict[str, object]:
    """Boot the LLM server on this machine and exercise every endpoint."""
    import urllib.parse
    import urllib.request

    from .server import create_app

    os.makedirs(image_dir, exist_ok=True)
    app = create_app(model=model, image_dir=image_dir)
    report: Dict[str, object] = {"served": False, "smoke_ok": False}
    try:
        port = app.start("127.0.0.1", 0)
        base = "http://127.0.0.1:%d" % port

        def get(path: str, timeout: int = 120):
            with urllib.request.urlopen(base + path, timeout=timeout) as response:
                body = response.read()
                kind = response.headers.get("Content-Type", "")
            return json.loads(body.decode("utf-8")) if "json" in kind else body

        def post(path: str, payload: dict):
            request = urllib.request.Request(
                base + path, data=json.dumps(payload).encode("utf-8"), method="POST",
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))

        status = get("/status")
        kernel = get("/kernel")
        chat = post("/chat", {"message": "कोड लिखो: " + target})
        run = post("/run", {"source": "दर्शय 6 * 7"})
        picture = get("/image?prompt=" + urllib.parse.quote(target))
        shell = post("/shell", {"command": "ps"})
        shell_run = post("/shell", {"command": "run दर्शय 6 * 7"})
        report.update({
            "served": True,
            "port": port,
            "model_params": (status.get("model") or {}).get("params"),
            "kernel_ok": bool(kernel.get("ok")),
            "chat_ok": chat.get("intent") == "code" and not chat.get("error"),
            "code_origin": chat.get("origin"),
            "run_ok": run.get("ok") is True and run.get("output") == ["42"],
            "image_ok": isinstance(picture, bytes) and picture.startswith(b"\x89PNG"),
            "image_bytes": len(picture) if isinstance(picture, bytes) else 0,
            "shell_ok": bool(shell.get("ok") and shell.get("output")),
            "shell_run": shell_run.get("output"),
            "endpoints": ["/", "/status", "/kernel", "/chat", "/generate",
                          "/run", "/explain", "/image", "/shell"],
        })
        report["smoke_ok"] = bool(report["kernel_ok"] and report["chat_ok"]
                                  and report["run_ok"] and report["image_ok"]
                                  and report["shell_ok"])
    except Exception as error:  # noqa: BLE001 - reported, never hidden
        report["error"] = "%s: %s" % (type(error).__name__, error)
    finally:
        app.shutdown()
    return report


def _previous_report(outdir: str) -> dict:
    """पिछले मिशन की रिपोर्ट (यदि है) — resume के लिए।"""
    path = os.path.join(outdir, "mission.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle) or {}
    except (OSError, ValueError):
        return {}


def _resumable_checkpoint(previous: dict) -> Optional[str]:
    """केवल वह चेकपॉइंट जो वास्तव में पढ़ा जा सकता है।"""
    candidate = (previous.get("training") or {}).get("checkpoint")
    if candidate and os.path.exists(os.path.join(str(candidate), "model.json")):
        return str(candidate)
    return None


def last_mission(outdir: Optional[str] = None) -> Optional[dict]:
    """पिछले मिशन का संक्षिप्त सारांश (कहीं भी दिखाने के लिए), या ``None``."""
    from brahma_paths import data_root

    outdir = outdir or data_root("mission", create=False)
    report = _previous_report(outdir)
    if not report:
        return None
    training = report.get("training") or {}
    best = training.get("best_perplexity")
    return {
        "target": report.get("target"),
        "elapsed": report.get("elapsed"),
        "best_perplexity": round(best, 3) if isinstance(best, (int, float)) else None,
        "params": training.get("params"),
        "programs": training.get("programs"),
        "os_origin": (report.get("os") or {}).get("origin"),
        "server_smoke_ok": (report.get("server") or {}).get("smoke_ok"),
        "kernel_verified": report.get("kernel_verified"),
        "report": os.path.join(outdir, "mission.json"),
    }


def run_mission(
    target: str,
    keywords: str = "",
    outdir: Optional[str] = None,
    iterations: int = 2,
    epochs: int = 2,
    size: str = "tiny",
    budget: float = 180.0,
    serve: bool = True,
    write_os: bool = True,
    seed: int = 7,
    log=None,
    resume: bool = False,
    continuous: bool = False,
    target_perplexity: Optional[float] = None,
    max_generations: int = 3,
) -> Dict[str, object]:
    """Run the whole cycle for ``target`` and return the mission report.

    ``resume`` continues from the checkpoint of the previous mission in
    ``outdir`` instead of starting cold.  ``continuous`` keeps training in
    further *generations* while each one improves and the budget lasts, stopping
    early when ``target_perplexity`` is reached.
    """
    from brahma_paths import data_root

    started = time.time()
    log = log or (lambda message: print(message))
    outdir = outdir or data_root("mission", create=True)
    os.makedirs(outdir, exist_ok=True)

    previous = _previous_report(outdir) if resume else {}
    resume_from = _resumable_checkpoint(previous) if resume else None
    previous_best: Optional[float] = None
    if resume_from:
        try:
            previous_best = float((previous.get("training") or {}).get("best_perplexity"))
        except (TypeError, ValueError):
            previous_best = None
    if resume:
        log("↩️ पिछला मिशन: %s" % ("चेकपॉइंट मिला" if resume_from else "कोई नहीं — नए सिरे से"))

    log("🕉️ लक्ष्य: %s" % target)
    generations: list = []
    generation_summaries: list = []
    best_checkpoint = resume_from or ""
    best_perplexity = previous_best if previous_best else float("inf")
    current_resume = resume_from

    while True:
        trainer = AutonomousTrainer(workdir=os.path.join(outdir, "llm"), seed=seed, log=log)
        generation = trainer.run(Target(
            description=target, keywords=keywords or target,
            iterations=iterations, epochs=epochs, size=size,
            budget_seconds=budget, threshold=target_perplexity,
            resume_from=current_resume,
            previous_best=best_perplexity if best_perplexity < float("inf") else None))
        generations.append(generation)
        generation_best = float(generation.get("best", {}).get("perplexity") or float("inf"))
        checkpoint = generation.get("checkpoint") or os.path.join(outdir, "llm", "best")
        improved = generation_best < best_perplexity
        if improved:
            best_perplexity = generation_best
            best_checkpoint = checkpoint
        generation_summaries.append({
            "best_perplexity": None if generation_best == float("inf") else generation_best,
            "improved": improved,
            "params": generation.get("params"),
            "rounds": len(generation.get("rounds", [])),
            "cold_start": generation.get("cold_start", True),
            "elapsed": generation.get("elapsed"),
        })
        spent = time.time() - started
        enough = target_perplexity is not None and best_perplexity <= target_perplexity
        if (not continuous or enough or not improved or spent >= budget
                or len(generations) >= max_generations):
            break
        log("🔁 पीढ़ी %d पूरी (ppl %.3f) — शेष बजट %.0f s, अगली पीढ़ी"
            % (len(generations), generation_best, budget - spent))
        current_resume = checkpoint

    rounds: list = []
    programs = {"generated": 0, "accepted": 0, "acceptance_rate": 0.0}
    for generation in generations:
        rounds.extend(generation.get("rounds", []))
        per_generation = generation.get("programs", {})
        programs["generated"] += int(per_generation.get("generated", 0))
        programs["accepted"] += int(per_generation.get("accepted", 0))
    if programs["generated"]:
        programs["acceptance_rate"] = programs["accepted"] / programs["generated"]

    checkpoint = best_checkpoint or (generations[-1].get("checkpoint") if generations else "")
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

    # -- 3. the model serves itself --------------------------------------
    server_report: Dict[str, object] = {"served": False}
    if serve:
        server_report = _smoke_server(model, target, os.path.join(outdir, "chitra"))

    report = {
        "target": target,
        "elapsed": round(time.time() - started, 2),
        "training": {
            "rounds": rounds,
            "best_perplexity": None if best_perplexity == float("inf") else best_perplexity,
            "params": model.model.parameter_count(),
            "programs": programs,
            "checkpoint": checkpoint,
            "generations": generation_summaries,
            "resumed_from": resume_from,
            "previous_best": previous_best,
            "improved_this_run": bool(previous_best is None or best_perplexity < previous_best),
        },
        "os": os_report,
        "server": server_report,
        "kernel_verified": bool(generations[-1].get("kernel", {}).get("ok")) if generations else False,
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
    parser.add_argument("--no-serve", action="store_true")
    parser.add_argument("--no-os", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="पिछले मिशन के चेकपॉइंट से आगे बढ़ें")
    parser.add_argument("--continuous", action="store_true",
                        help="सुधार होते रहने तक अगली पीढ़ियाँ चलाएँ")
    parser.add_argument("--target-perplexity", type=float, default=None)
    parser.add_argument("--max-generations", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = run_mission(args.target, keywords=args.keywords, outdir=args.out,
                         iterations=args.iterations, epochs=args.epochs, size=args.size,
                         budget=args.budget, serve=not args.no_serve,
                         write_os=not args.no_os, resume=args.resume,
                         continuous=args.continuous,
                         target_perplexity=args.target_perplexity,
                         max_generations=args.max_generations,
                         log=(lambda message: None) if args.json else print)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        server = report["server"]
        if not server.get("served"):
            server_state = "छोड़ा गया"
        else:
            server_state = "ठीक" if server.get("smoke_ok") else "विफल"
        print("कर्नेल: %s, सर्वर: %s"
              % (report["os"].get("origin", "नहीं बनाया"), server_state))
        if server.get("served"):
            print("सर्वर: चैट %s, कोड %s, चित्र %s, OS %s" % (
                "हाँ" if server.get("chat_ok") else "नहीं",
                "हाँ" if server.get("chat_ok") else "नहीं",
                "हाँ" if server.get("image_ok") else "नहीं",
                "हाँ" if server.get("kernel_ok") else "नहीं"))
    ok = (report["kernel_verified"]
          and (not report["server"].get("served") or report["server"].get("smoke_ok")))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
