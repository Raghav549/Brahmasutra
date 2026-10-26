"""🕉️ अनुप्रयोग निर्माता — the app builder, driven by ब्रह्म-LLM.

This replaces the old generators that wrote HTML placeholders, printed
*"Installable APK निर्मित"* and produced files nobody could run.  The new
builder produces a bundle that is **executed before it is handed over**:

``<name>.sutra``
    The application logic, written *in सूत्र* by the language model and then
    compiled + run.  If the model's output does not run, the builder says so in
    the manifest and falls back to a validated template program.
``server.py``
    A dependency-free HTTP server (:mod:`brahma_web`) exposing ``/``, ``/logic``,
    ``/run`` and ``/status``.  ``/run`` executes the सूत्र program on the
    project's VM, so the web layer and the language really are connected.
``index.html``
    A one-page UI that posts to ``/run``.
``manifest.json``
    Provenance: the target, the model that wrote the programs, parameter count,
    whether the logic was generated or fell back, and the smoke-test result.

``python3 -m brahma_llm.app_builder --target "प्राइम जाँच" --json`` prints the
manifest; ``brahma llm build-app`` is the same thing from the main CLI.
"""

from __future__ import annotations

import json
import os
import time
import unicodedata
import urllib.request
from typing import Dict, Optional, Sequence

SERVER_TEMPLATE = '''"""🕉️ {name} — ब्रह्म-LLM द्वारा निर्मित अनुप्रयोग (मानक लाइब्रेरी केवल)."""

from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def _import_brahma():
    """Import the engine — from the installed package or the source checkout."""
    try:
        from brahma.api import execute as _execute
        from brahma_web import App as _App
        return _execute, _App
    except ImportError:
        pass
    root = _HERE
    while True:
        if os.path.exists(os.path.join(root, "brahma_web.py")):
            sys.path.insert(0, root)
            from brahma.api import execute as _execute
            from brahma_web import App as _App
            return _execute, _App
        parent = os.path.dirname(root)
        if parent == root:
            raise ImportError(
                "brahma_web नहीं मिला — `pip install .` करें या रिपॉज़िटरी रूट से चलाएँ"
            )
        root = parent


execute, App = _import_brahma()
from brahma_web import Response, json_response, text_response  # noqa: E402

LOGIC = os.path.join(_HERE, "{logic_file}")
INDEX = os.path.join(_HERE, "index.html")
STEP_LIMIT = {step_limit}


def read_logic() -> str:
    with open(LOGIC, "r", encoding="utf-8") as handle:
        return handle.read()


def run_logic() -> dict:
    result = execute(read_logic(), source_name=LOGIC, step_limit=STEP_LIMIT)
    return {{
        "ok": result.error is None,
        "output": result.output,
        "error": None if result.error is None else str(result.error),
        "steps": result.steps,
        "elapsed": round(result.elapsed, 5),
    }}


def create_app() -> App:
    app = App("{name}")

    @app.route("/")
    def index(_request):
        if os.path.exists(INDEX):
            with open(INDEX, "r", encoding="utf-8") as handle:
                return Response(status=200, payload=handle.read(),
                                headers={{"Content-Type": "text/html; charset=utf-8"}})
        return text_response("index.html अनुपस्थित")

    @app.route("/logic")
    def logic(_request):
        return text_response(read_logic())

    @app.route("/run", methods=("GET", "POST"))
    def run(_request):
        return json_response(run_logic())

    @app.route("/status")
    def status(_request):
        report = run_logic()
        return json_response({{"app": "{name}", "engine": "BRAHMA", "ok": report["ok"],
                              "steps": report["steps"], "lines": len(report["output"])}})

    return app


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default={port})
    parser.add_argument("--once", action="store_true", help="पोर्ट बाँधकर तुरंत बंद करें")
    args = parser.parse_args(argv)
    app = create_app()
    if args.once:
        bound = app.start(args.host, args.port)
        app.shutdown()
        print("{{}} पोर्ट {{}} पर तैयार".format("{name}", bound))
        return 0
    print("🕉️ {name} — http://%s:%d" % (args.host, args.port))
    app.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

INDEX_TEMPLATE = """<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<title>{name}</title>
<style>
 body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 46rem; line-height: 1.5; }}
 pre {{ background: #111; color: #eee; padding: 1rem; overflow-x: auto; border-radius: 8px; }}
 button {{ font-size: 1rem; padding: .5rem 1rem; border-radius: 6px; }}
 .muted {{ color: #666; font-size: .9rem; }}
</style>
</head>
<body>
<h1>🕉️ {name}</h1>
<p class="muted">लक्ष्य: {target}</p>
<p class="muted">यह पृष्ठ <code>{logic_file}</code> को ब्रह्म VM पर चलाता है।</p>
<button id="run">चलाएँ</button>
<h2>प्रोग्राम</h2>
<pre id="logic">लोड हो रहा है…</pre>
<h2>आउटपुट</h2>
<pre id="out">—</pre>
<script>
async function load() {{
  const text = await (await fetch('/logic')).text();
  document.getElementById('logic').textContent = text;
}}
async function run() {{
  const box = document.getElementById('out');
  box.textContent = 'चल रहा है…';
  const data = await (await fetch('/run', {{method: 'POST'}})).json();
  box.textContent = data.ok ? data.output.join('\\n') : ('त्रुटि: ' + data.error);
}}
document.getElementById('run').addEventListener('click', run);
load();
</script>
</body>
</html>
"""

README_TEMPLATE = """# {name}

🕉️ ब्रह्म-LLM द्वारा निर्मित अनुप्रयोग।

* लक्ष्य: {target}
* तर्क (सूत्र): `{logic_file}` — {logic_origin}
* सर्वर: `server.py` (मानक लाइब्रेरी, कोई Flask नहीं)

```bash
python server.py --port {port}     # खोलें: http://127.0.0.1:{port}/
python server.py --once            # पोर्ट बाँधकर जाँच
curl -s localhost:{port}/run | head
```

Smoke test: {smoke}
"""


def slug(text: str, fallback: str = "app") -> str:
    """Filesystem-safe name that keeps Devanagari (matras included)."""
    kept = []
    for character in (text or "").strip():
        if character.isalnum() or unicodedata.category(character) in ("Mn", "Mc"):
            kept.append(character)
        elif character in "-_ ":
            kept.append("_")
    name = "".join(kept).strip("_")
    while "__" in name:
        name = name.replace("__", "_")
    return (name or fallback)[:48]


def _fallback_logic(target: str) -> str:
    """A validated program used when generated code does not run."""
    return (
        "# लक्ष्य: %s\n"
        'दर्शय "🕉️ अनुप्रयोग तैयार"\n'
        "कार्य योग(a, b)\n    प्रत्यागमन a + b\nअन्त\n"
        "दर्शय योग(2, 3)\n" % target
    )


def _write(path: str, text: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def run_smoke(app_dir: str, name: str) -> Dict[str, object]:
    """Import the generated ``server.py`` and exercise its endpoints."""
    import importlib.util

    server_path = os.path.join(app_dir, "server.py")
    spec = importlib.util.spec_from_file_location("builtin_%s_server" % name, server_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    app = module.create_app()
    port = app.start("127.0.0.1", 0)
    base = "http://127.0.0.1:%d" % port
    checks = {}
    try:
        with urllib.request.urlopen(base + "/status", timeout=10) as response:
            checks["status"] = json.loads(response.read().decode("utf-8"))
        request = urllib.request.Request(base + "/run", data=b"", method="POST")
        with urllib.request.urlopen(request, timeout=10) as response:
            checks["run"] = json.loads(response.read().decode("utf-8"))
        with urllib.request.urlopen(base + "/", timeout=10) as response:
            checks["index_bytes"] = len(response.read())
    finally:
        app.shutdown()
    checks["ok"] = bool(checks.get("status", {}).get("ok")) and bool(checks.get("run", {}).get("ok"))
    return checks


def generate_app(
    model,
    target: str,
    outdir: Optional[str] = None,
    name: Optional[str] = None,
    port: int = 8000,
    step_limit: int = 200_000,
    smoke: bool = True,
    generate: bool = True,
) -> Dict[str, object]:
    """Build, validate and return an app bundle; ``model`` may be ``None``."""
    from brahma.api import execute

    from .programs import ProgramGenerator

    name = name or slug(target, "brahma_app")
    if outdir is None:
        from brahma_paths import data_root

        outdir = data_root("apps", name, create=True)
    app_dir = os.path.abspath(outdir)
    os.makedirs(app_dir, exist_ok=True)

    # 1. logic — the model writes सूत्र, and we keep only code that runs
    logic_origin = "generated" if (generate and model is not None) else "fallback (no model)"
    logic_source = ""
    if generate and model is not None:
        try:
            logic_source = model.complete_program("# लक्ष्य: %s\n" % target, max_tokens=90, seed=11)
        except Exception as error:  # model may be untrained/empty
            logic_source = ""
            logic_origin = "generated-invalid: %s" % error
    program_report = execute(logic_source, source_name="<app>", step_limit=step_limit) if logic_source.strip() else None
    if program_report is None or program_report.error is not None:
        if logic_origin == "generated":
            logic_origin = "fallback (generated code did not compile)"
        candidate = ProgramGenerator(seed=len(target)).passing(target, count=4)
        logic_source = candidate[0].source if candidate else _fallback_logic(target)
        program_report = execute(logic_source, source_name="<app>", step_limit=step_limit)
        if program_report.error is not None:
            logic_source = _fallback_logic(target)
            logic_origin = "fallback-template"
            program_report = execute(logic_source, source_name="<app>", step_limit=step_limit)

    logic_file = "%s.sutra" % slug(name, "app")
    _write(os.path.join(app_dir, logic_file), logic_source)

    # 2. server + UI + docs
    _write(os.path.join(app_dir, "server.py"), SERVER_TEMPLATE.format(
        name=name, logic_file=logic_file, port=port, step_limit=step_limit))
    _write(os.path.join(app_dir, "index.html"), INDEX_TEMPLATE.format(
        name=name, target=target, logic_file=logic_file))

    # 3. smoke test the real server
    smoke_report: Dict[str, object] = {"ok": False, "skipped": True}
    if smoke:
        try:
            smoke_report = run_smoke(app_dir, name)
        except Exception as error:  # noqa: BLE001 - reported, never hidden
            smoke_report = {"ok": False, "error": "%s: %s" % (type(error).__name__, error)}

    manifest = {
        "name": name,
        "target": target,
        "dir": app_dir,
        "logic_file": logic_file,
        "logic_origin": logic_origin,
        "logic_runs": program_report.error is None,
        "logic_output": program_report.output,
        "logic_error": None if program_report.error is None else str(program_report.error),
        "smoke": smoke_report,
        "engine": "BRAHMA",
        "model": None if model is None else {
            "kind": model.model.kind,
            "params": model.model.parameter_count(),
            "vocab": model.tokenizer.vocab_size,
            "size": model.size,
        },
        "created": time.time(),
        "port": port,
    }
    _write(os.path.join(app_dir, "manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=1))
    _write(os.path.join(app_dir, "README.md"), README_TEMPLATE.format(
        name=name, target=target, logic_file=logic_file, logic_origin=logic_origin,
        port=port, smoke="ठीक" if smoke_report.get("ok") else "विफल: %s" % smoke_report))
    return manifest


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="ब्रह्म-LLM अनुप्रयोग निर्माता")
    parser.add_argument("--target", default="नमस्ते विश्व अनुप्रयोग")
    parser.add_argument("--name", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model", default=None, help="चेकपॉइंट निर्देशिका")
    parser.add_argument("--no-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    model = None
    if args.model:
        from .model import BrahmaLLM

        model = BrahmaLLM.load(args.model)
    manifest = generate_app(model, args.target, outdir=args.out, name=args.name,
                            port=args.port, smoke=not args.no_smoke)
    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=1, default=str))
    else:
        print("🕉️ अनुप्रयोग: %s" % manifest["dir"])
        print("  तर्क: %s (%s)" % (manifest["logic_file"], manifest["logic_origin"]))
        print("  smoke: %s" % ("ठीक" if manifest["smoke"].get("ok") else manifest["smoke"]))
    return 0 if manifest["logic_runs"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
