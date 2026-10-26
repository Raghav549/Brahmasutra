"""🕉️ एकीकृत CLI — ``brahma llm <command>``.

Every subsystem built in this package is reachable from here, so the pieces are
connected instead of being separate demos:

======================  =====================================================
command                 what it actually does
======================  =====================================================
``info``                model + corpus + kernel summary
``corpus``              corpus statistics and a sample of the texts
``train``               train once on the repository corpus and save
``generate``            sample text (Python engine or सूत्र VM engine)
``complete``            sample a **sूत्र program and keep the valid part**
``chat``                small interactive loop (REPL)
``autotrain``           set a target and run the autonomous loop
``evolve``              one self-edit round (body growth / OS reinstall)
``kernel``              build, boot, verify or install the सूत्र-OS image
``ask`` / ``chat``      the model answers: chat, code, run, explain, image
``serve``              serve the model itself over HTTP (chat/code/image/kernel)
``sutra-math``          prove the model's maths on the सूत्र VM
``bench``               measured perplexity/speed table (no invented numbers)
======================  =====================================================
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional, Sequence


#: Every size preset the model knows about, largest last.
SIZES = ("tiny", "small", "medium", "large", "xlarge", "huge", "brahma")


def _model_dir(path: Optional[str]) -> str:
    from brahma_paths import data_root

    return path or data_root("llm", "best")


def _load_model(path: Optional[str]):
    from .model import BrahmaLLM

    directory = _model_dir(path)
    if not os.path.isdir(directory):
        raise SystemExit("कोई चेकपॉइंट नहीं: %s\nपहले `brahma llm train` चलाएँ।" % directory)
    return BrahmaLLM.load(directory)


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------
def cmd_info(args: argparse.Namespace) -> int:
    from .kernel import verify
    from .programs import load_corpus, sutra_files

    info = {"model_dir": _model_dir(args.model)}
    try:
        model = _load_model(args.model)
        info["model"] = model.info()
    except SystemExit as error:
        info["model"] = {"error": str(error)}
    kernel = verify()
    info["kernel"] = {"ok": kernel["ok"], "steps": kernel["steps"], "image_bytes": kernel["image_bytes"]}
    info["corpus"] = {"sutra_files": len(sutra_files()), "texts": len(load_corpus(include_docs=False))}
    from .mission import last_mission

    info["mission"] = last_mission()
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=1, default=str))
        return 0
    print("🕉️ ब्रह्म-LLM")
    model_info = info["model"]
    if "error" in model_info:
        print("  मॉडल: %s" % model_info["error"])
    else:
        print("  मॉडल: %s / %s, %s पैरामीटर, शब्दावली %s"
              % (model_info["kind"], model_info["size"], model_info["params"], model_info["vocab_size"]))
    print("  कर्नेल: %s (%d बाइट, %d चरण)"
          % ("ठीक" if kernel["ok"] else "विफल", kernel["image_bytes"], kernel["steps"]))
    print("  कॉर्पस: %d सूत्र फ़ाइलें, %d प्रशिक्षण पाठ"
          % (info["corpus"]["sutra_files"], info["corpus"]["texts"]))
    mission = info.get("mission")
    if mission:
        print("  पिछला मिशन: %s — ppl %s, सर्वर %s, OS %s"
              % (mission.get("target"), mission.get("best_perplexity"),
                 "ठीक" if mission.get("server_smoke_ok") else "—",
                 mission.get("os_origin")))
    return 0


def cmd_corpus(args: argparse.Namespace) -> int:
    from .programs import (ProgramGenerator, generated_dir, load_corpus,
                           save_generated, sutra_files)

    written = []
    if getattr(args, "generate", 0):
        generator = ProgramGenerator(seed=args.seed)
        programs = generator.passing(goal=args.goal, count=args.generate)
        outdir = args.out or generated_dir()
        existing = 0
        if os.path.isdir(outdir):
            existing = len([name for name in os.listdir(outdir) if name.endswith(".sutra")])
        written = save_generated([p.source for p in programs], outdir=outdir,
                                 start=existing + 1)
        if not args.json:
            print("बनाए गए कार्यक्रम: %d/%d → %s"
                  % (len(written), args.generate, outdir))

    files = sutra_files()
    corpus = load_corpus()
    stats = {
        "generated_written": len(written),
        "sutra_files": len(files),
        "texts": len(corpus),
        "characters": sum(len(text) for text in corpus),
        "devanagari_chars": sum("\u0900" <= ch <= "\u097f" for text in corpus for ch in text),
        "sample": corpus[: args.sample],
    }
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=1))
        return 0
    print("कॉर्पस: %d फ़ाइलें, %d पाठ, %d अक्षर (%d देवनागरी)"
          % (stats["sutra_files"], stats["texts"], stats["characters"], stats["devanagari_chars"]))
    for text in corpus[: args.sample]:
        print("---\n%s" % text.strip()[:400])
    return 0


def cmd_train(args: argparse.Namespace) -> int:
    import time

    from .model import BrahmaLLM
    from .programs import load_corpus

    started = time.time()
    corpus = load_corpus(include_docs=args.docs)
    model = BrahmaLLM.create(kind=args.kind, size=args.size, seed=args.seed)
    model.fit(corpus, epochs=args.epochs,
              on_epoch=None if args.json else (lambda epoch, loss: print("  epoch %2d  loss %.4f" % (epoch + 1, loss))))
    metrics = model.evaluate(corpus[::5])
    out = args.out or _model_dir(None)
    model.save(out)
    elapsed = time.time() - started
    report = {"model": model.info(), "out": out, "holdout_perplexity": metrics["perplexity"],
              "train_texts": len(corpus), "elapsed_seconds": round(elapsed, 2),
              "epochs": args.epochs}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        print("🕉️ प्रशिक्षण पूर्ण: %s" % out)
        print("  पैरामीटर: %d, perplexity: %.3f, समय: %.1f s (%d epoch)"
              % (report["model"]["params"], metrics["perplexity"], elapsed, args.epochs))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    model = _load_model(args.model)
    if args.engine == "sutra":
        from .sutra_kernel import sutra_generate

        text = sutra_generate(model.model, model.tokenizer, args.prompt,
                              max_tokens=args.tokens, temperature=args.temperature, seed=args.seed)
    else:
        text = model.generate(args.prompt, max_tokens=args.tokens,
                              temperature=args.temperature, seed=args.seed)
    print(text)
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    model = _load_model(args.model)
    program = model.complete_program(args.prompt, max_tokens=args.tokens, seed=args.seed)
    print(program)
    return 0 if program.strip() else 1


def cmd_autotrain(args: argparse.Namespace) -> int:
    from .trainer import AutonomousTrainer, Target

    target = Target(description=args.target, keywords=args.keywords or args.target,
                    iterations=args.iterations, epochs=args.epochs, size=args.size,
                    kind=args.kind, budget_seconds=args.budget, threshold=args.threshold)
    trainer = AutonomousTrainer(workdir=args.workdir,
                                log=(lambda message: None) if args.json else print)
    report = trainer.run(target)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        print("रिपोर्ट: %s" % report["report_path"])
    return 0


def cmd_evolve(args: argparse.Namespace) -> int:
    from .selfedit import SelfEditor

    model = _load_model(args.model)
    editor = SelfEditor(workdir=args.workdir)
    results = []
    if args.body:
        contexts = [model.tokenizer.encode(text)[:4] for text in
                    ("दर्शय अ", "स्थापय अ = १०", "यदि अ > ५")]
        contexts = [context for context in contexts if context]
        before = model.model.parameter_count()
        record = editor.try_grow(model.model, contexts, extra=args.extra)
        if record.accepted:
            model.save(_model_dir(args.model))
        results.append({"body": record.as_dict(), "params_before": before,
                        "params_after": model.model.parameter_count()})
    if args.os:
        from .kernel import KERNEL_SOURCE

        results.append({"os": editor.try_os(KERNEL_SOURCE).as_dict()})
    editor.flush()
    payload = {"edits": results, "log": editor.log_path}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=1, default=str))
    else:
        for entry in results:
            for kind, record in entry.items():
                if isinstance(record, dict):
                    print("  %-12s %s → %s" % (kind, record.get("description", ""),
                                               "स्वीकृत" if record.get("accepted") else "अस्वीकृत"))
    return 0


def cmd_kernel(args: argparse.Namespace) -> int:
    from . import kernel

    if args.kernel_action == "install":
        print("स्थापित: %s" % kernel.install())
        return 0
    if args.kernel_action == "build":
        target = args.out or kernel.image_path()
        with open(target, "wb") as handle:
            handle.write(kernel.build_image())
        print("image: %s" % target)
        return 0
    if args.kernel_action == "info":
        return kernel.main(["info", "--json"] if args.json else ["info"])
    report = kernel.verify() if args.kernel_action == "verify" else kernel.boot()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
        return 0 if report.get("ok", True) else 1
    for line in report["output"]:
        print(line)
    return 0 if report.get("ok", True) else 1


def cmd_shell(args: argparse.Namespace) -> int:
    from .shell import main as shell_main

    argv: List[str] = []
    for command in args.command:
        argv.extend(["--command", command])
    if args.script:
        argv.extend(["--script", args.script])
    if args.json:
        argv.append("--json")
    if args.quiet:
        argv.append("--quiet")
    return shell_main(argv)


def cmd_ask(args: argparse.Namespace) -> int:
    from .agent import BrahmaAgent

    checkpoint = None if args.no_model else _model_dir(args.model)
    if checkpoint and not os.path.isdir(checkpoint):
        checkpoint = None
    agent = BrahmaAgent(checkpoint=checkpoint)
    message = " ".join(args.message) if isinstance(args.message, list) else args.message
    result = agent.respond(message, image_path=args.out)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1, default=str))
    else:
        print(result.get("text", ""))
    return 0 if result.get("error") in (None, "") else 1


def cmd_chat(args: argparse.Namespace) -> int:
    from .agent import BrahmaAgent

    checkpoint = None if args.no_model else _model_dir(args.model)
    if checkpoint and not os.path.isdir(checkpoint):
        checkpoint = None
    agent = BrahmaAgent(checkpoint=checkpoint)
    print("🕉️ ब्रह्म-LLM — बातचीत (`बाहर`/`exit` से बाहर)")
    while True:
        try:
            message = input("आप › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not message or message in ("बाहर", "exit", "quit"):
            break
        result = agent.respond(message)
        print("ब्रह्म › " + str(result.get("text", "")).strip())
    return 0


def cmd_image(args: argparse.Namespace) -> int:
    from .agent import BrahmaAgent

    checkpoint = None if args.no_model else _model_dir(args.model)
    if checkpoint and not os.path.isdir(checkpoint):
        checkpoint = None
    agent = BrahmaAgent(checkpoint=checkpoint)
    result = agent.image(args.prompt, path=args.out)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1, default=str))
    else:
        print(result["text"])
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from .server import create_app

    checkpoint = None if args.no_model else _model_dir(args.model)
    if checkpoint and not os.path.isdir(checkpoint):
        checkpoint = None
    app = create_app(checkpoint=checkpoint, image_dir=args.image_dir,
                     allow_train=args.allow_train)
    if args.once:
        bound = app.start("127.0.0.1", args.port)
        app.shutdown()
        print("🕉️ ब्रह्म-LLM पोर्ट %d पर तैयार" % bound)
        return 0
    print("🕉️ ब्रह्म-LLM — http://%s:%d" % (args.host, args.port))
    app.serve(args.host, args.port)
    return 0


def cmd_mission(args: argparse.Namespace) -> int:
    from .mission import run_mission

    report = run_mission(args.target, keywords=args.keywords, outdir=args.out,
                         iterations=args.iterations, epochs=args.epochs, size=args.size,
                         budget=args.budget, serve=not args.no_serve,
                         write_os=not args.no_os, resume=args.resume,
                         continuous=args.continuous,
                         target_perplexity=args.target_perplexity,
                         max_generations=args.max_generations, grow=args.grow,
                         log=(lambda message: None) if args.json else print)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        print("रिपोर्ट: %s" % report["report_path"])
    ok = (report["kernel_verified"]
          and (not report["server"]["served"] or report["server"]["smoke_ok"]))
    return 0 if ok else 1


def cmd_sutra_math(args: argparse.Namespace) -> int:
    from . import sutra_kernel

    return sutra_kernel.main(["--check"] + (["--json"] if args.json else []))


def cmd_bench(args: argparse.Namespace) -> int:
    from .model import BrahmaLLM
    from .programs import load_corpus

    corpus = load_corpus(include_docs=False)
    holdout = corpus[::5][:10]
    train = [text for index, text in enumerate(corpus) if index % 5 != 0]
    rows = []
    for kind in ("ngram", "neural"):
        for size in args.sizes:
            import time

            started = time.time()
            model = BrahmaLLM.create(kind=kind, size=size, seed=args.seed)
            model.fit(train, epochs=args.epochs)
            metrics = model.evaluate(holdout)
            rows.append({
                "kind": kind,
                "size": size,
                "params": model.model.parameter_count(),
                "vocab": model.tokenizer.vocab_size,
                "perplexity": round(metrics["perplexity"], 3),
                "seconds": round(time.time() - started, 2),
            })
    import math

    uniform = math.log(max(2, rows[0]["vocab"])) if rows else 0.0
    if args.json:
        print(json.dumps({"rows": rows, "train_texts": len(train), "holdout_texts": len(holdout),
                          "uniform_baseline": round(uniform, 3)}, ensure_ascii=False, indent=1))
        return 0
    print("(uniform baseline perplexity = %.1f)" % math.exp(uniform))
    print("%-8s %-7s %10s %6s %12s %8s" % ("kind", "size", "params", "vocab", "perplexity", "seconds"))
    print("%-8s %-7s %10s %6s %12s %8s" % ("-" * 8, "-" * 7, "-" * 10, "-" * 6, "-" * 12, "-" * 8))
    for row in rows:
        print("%-8s %-7s %10d %6d %12.3f %8.2f"
              % (row["kind"], row["size"], row["params"], row["vocab"], row["perplexity"], row["seconds"]))
    return 0


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brahma llm", description="ब्रह्म-LLM")
    sub = parser.add_subparsers(dest="command")

    info = sub.add_parser("info", help="मॉडल/कॉर्पस/कर्नेल सारांश")
    info.add_argument("--model", default=None)
    info.add_argument("--json", action="store_true")
    info.set_defaults(func=cmd_info)

    corpus = sub.add_parser("corpus", help="कॉर्पस आँकड़े")
    corpus.add_argument("--json", action="store_true")
    corpus.add_argument("--sample", type=int, default=2)
    corpus.add_argument("--generate", type=int, default=0,
                        help="इतने वैध सूत्र कार्यक्रम बनाकर कॉर्पस में लिखें")
    corpus.add_argument("--goal", default="")
    corpus.add_argument("--seed", type=int, default=0)
    corpus.add_argument("--out", default=None)
    corpus.set_defaults(func=cmd_corpus)

    train = sub.add_parser("train", help="एक बार प्रशिक्षित करें")
    train.add_argument("--kind", default="neural", choices=("neural", "ngram"))
    train.add_argument("--size", default="tiny", choices=SIZES)
    train.add_argument("--epochs", type=int, default=None)
    train.add_argument("--seed", type=int, default=7)
    train.add_argument("--docs", action="store_true", help="दस्तावेज़-गद्य भी शामिल करें")
    train.add_argument("--out", default=None)
    train.add_argument("--json", action="store_true")
    train.set_defaults(func=cmd_train)

    generate = sub.add_parser("generate", help="पाठ उत्पन्न करें")
    generate.add_argument("prompt")
    generate.add_argument("--model", default=None)
    generate.add_argument("--tokens", type=int, default=60)
    generate.add_argument("--temperature", type=float, default=0.9)
    generate.add_argument("--seed", type=int, default=None)
    generate.add_argument("--engine", default="python", choices=("python", "sutra"))
    generate.set_defaults(func=cmd_generate)

    complete = sub.add_parser("complete", help="वैध सूत्र कार्यक्रम उत्पन्न करें")
    complete.add_argument("prompt", nargs="?", default="# कार्यक्रम\n")
    complete.add_argument("--model", default=None)
    complete.add_argument("--tokens", type=int, default=90)
    complete.add_argument("--seed", type=int, default=None)
    complete.set_defaults(func=cmd_complete)

    autotrain = sub.add_parser("autotrain", help="लक्ष्य + स्वायत्त प्रशिक्षण")
    autotrain.add_argument("--target", required=True)
    autotrain.add_argument("--keywords", default="")
    autotrain.add_argument("--iterations", type=int, default=3)
    autotrain.add_argument("--epochs", type=int, default=3)
    autotrain.add_argument("--size", default="tiny", choices=SIZES)
    autotrain.add_argument("--kind", default="neural", choices=("neural", "ngram"))
    autotrain.add_argument("--budget", type=float, default=180.0)
    autotrain.add_argument("--threshold", type=float, default=None)
    autotrain.add_argument("--workdir", default=None)
    autotrain.add_argument("--json", action="store_true")
    autotrain.set_defaults(func=cmd_autotrain)

    evolve = sub.add_parser("evolve", help="आत्म-संपादन (body / OS)")
    evolve.add_argument("--model", default=None)
    evolve.add_argument("--body", action="store_true")
    evolve.add_argument("--os", action="store_true")
    evolve.add_argument("--extra", type=int, default=4)
    evolve.add_argument("--workdir", default=None)
    evolve.add_argument("--json", action="store_true")
    evolve.set_defaults(func=cmd_evolve)

    kernel = sub.add_parser("kernel", help="सूत्र-OS कर्नेल")
    kernel.add_argument("kernel_action", nargs="?", default="verify",
                        choices=("build", "boot", "verify", "install", "info"))
    kernel.add_argument("--out", default=None)
    kernel.add_argument("--json", action="store_true")
    kernel.set_defaults(func=cmd_kernel)

    shell = sub.add_parser("shell", help="सूत्र-OS शेल (कर्नेल स्वयं आदेश चलाता है)")
    shell.add_argument("--command", "-c", action="append", default=[])
    shell.add_argument("--script", default=None)
    shell.add_argument("--json", action="store_true")
    shell.add_argument("--quiet", action="store_true")
    shell.set_defaults(func=cmd_shell)

    ask = sub.add_parser("ask", help="मॉडल से पूछें (चैट/कोड/चित्र/स्थिति)")
    ask.add_argument("message", nargs="+")
    ask.add_argument("--model", default=None)
    ask.add_argument("--out", default=None, help="चित्र फ़ाइल")
    ask.add_argument("--no-model", action="store_true")
    ask.add_argument("--json", action="store_true")
    ask.set_defaults(func=cmd_ask)

    chat = sub.add_parser("chat", help="अन्तःक्रियात्मक बातचीत")
    chat.add_argument("--model", default=None)
    chat.add_argument("--no-model", action="store_true")
    chat.set_defaults(func=cmd_chat)

    picture = sub.add_parser("image", help="मॉडल-चालित चित्र (PNG)")
    picture.add_argument("prompt")
    picture.add_argument("--out", default=None)
    picture.add_argument("--model", default=None)
    picture.add_argument("--no-model", action="store_true")
    picture.add_argument("--json", action="store_true")
    picture.set_defaults(func=cmd_image)

    serve = sub.add_parser("serve", help="मॉडल को HTTP पर परोसें")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8080)
    serve.add_argument("--model", default=None)
    serve.add_argument("--image-dir", default=None)
    serve.add_argument("--allow-train", action="store_true")
    serve.add_argument("--no-model", action="store_true")
    serve.add_argument("--once", action="store_true")
    serve.set_defaults(func=cmd_serve)

    mission = sub.add_parser(
        "mission", help="लक्ष्य → प्रशिक्षण → आत्म-संपादन → OS → चलता सर्वर")
    mission.add_argument("--target", required=True)
    mission.add_argument("--keywords", default="")
    mission.add_argument("--iterations", type=int, default=2)
    mission.add_argument("--epochs", type=int, default=2)
    mission.add_argument("--size", default="tiny", choices=SIZES)
    mission.add_argument("--budget", type=float, default=180.0)
    mission.add_argument("--out", default=None)
    mission.add_argument("--no-serve", action="store_true",
                         help="सर्वर smoke test छोड़ें")
    mission.add_argument("--no-os", action="store_true")
    mission.add_argument("--resume", action="store_true",
                         help="पिछले मिशन के चेकपॉइंट से आगे बढ़ें")
    mission.add_argument("--continuous", action="store_true",
                         help="सुधार होते रहने तक अगली पीढ़ियाँ चलाएँ")
    mission.add_argument("--target-perplexity", type=float, default=None)
    mission.add_argument("--max-generations", type=int, default=3)
    mission.add_argument("--grow", type=int, default=0,
                         help="प्रशिक्षण से पहले इतने नए वैध कार्यक्रम कॉर्पस में जोड़ें")
    mission.add_argument("--json", action="store_true")
    mission.set_defaults(func=cmd_mission)

    math = sub.add_parser("sutra-math", help="सूत्र-गणित प्रमाण")
    math.add_argument("--json", action="store_true")
    math.set_defaults(func=cmd_sutra_math)

    bench = sub.add_parser("bench", help="मापा गया बेंचमार्क")
    bench.add_argument("--sizes", nargs="+", default=["tiny", "small"])
    bench.add_argument("--epochs", type=int, default=3)
    bench.add_argument("--seed", type=int, default=7)
    bench.add_argument("--json", action="store_true")
    bench.set_defaults(func=cmd_bench)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    try:
        return int(args.func(args))
    except FileNotFoundError as error:
        sys.stderr.write("त्रुटि: फ़ाइल नहीं मिली: %s\n" % error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
