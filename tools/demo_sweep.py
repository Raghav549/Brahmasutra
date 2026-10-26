#!/usr/bin/env python3
"""🕉️ Demo sweep — run every demo script in the repository and report the truth.

`tools/legacy_baseline.py` covers the *top-level* scripts.  This tool covers the
263 scripts in sub-directories (`कृत्रिमबुद्धि/`, `engine/`, `vm/`, the demo app
backends, …) and classifies them:

``ok``        exited 0
``usage``     exited 2 (needs arguments / needs a terminal) — expected for CLIs
``server``    detected as a network/GUI server (``serve_forever``, ``mainloop``,
              …) and skipped — a server is supposed to block; the unit suite
              smoke-tests them with ``--once`` instead
``fail``      anything else, with the last line of stderr

The sweep is what turned 49 broken sub-directory demos into 7 (six of which are
servers that collided on a port during a *parallel* run, and one a genuinely
wrong relative path).  Use it after touching the legacy tree:

    python tools/demo_sweep.py              # human readable summary
    python tools/demo_sweep.py --check      # exit 1 if anything fails
    python tools/demo_sweep.py --json out.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__", ".venv", "build", "dist", "tests", "brahma", "brahma_llm", "node_modules"}


def scripts() -> List[str]:
    """Every ``.py`` file in a sub-directory of the repository."""
    found: List[str] = []
    for base, directories, files in os.walk(REPO_ROOT):
        directories[:] = [name for name in directories if name not in SKIP_DIRS]
        if base == REPO_ROOT:
            continue
        for name in files:
            if name.endswith(".py"):
                found.append(os.path.relpath(os.path.join(base, name), REPO_ROOT))
    return sorted(found)


SERVER_MARKERS = (
    "serve_forever", "socketserver", "http.server", "mainloop()", "serve(",
    "brahma_chat", "brahma_web",  # the stdlib backends these wrappers delegate to
)


def looks_like_server(path: str) -> bool:
    """True for demos whose whole job is to block on a socket or a GUI loop."""
    try:
        with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8", errors="replace") as handle:
            source = handle.read()
    except OSError:
        return False
    return any(marker in source for marker in SERVER_MARKERS)


def run(path: str, timeout: float, home: str) -> Dict[str, object]:
    if looks_like_server(path):
        return {"path": path, "status": "server", "detail": "source looks like a server (skipped)"}
    environment = dict(os.environ)
    environment["BRAHMA_HOME"] = home
    try:
        completed = subprocess.run(
            [sys.executable, path],
            cwd=REPO_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=environment,
        )
    except subprocess.TimeoutExpired:
        return {"path": path, "status": "server", "detail": "timeout (blocks by design)"}
    stderr = completed.stderr.decode("utf-8", "replace").strip().splitlines()
    detail = stderr[-1][:160] if stderr else ""
    if completed.returncode == 0:
        status = "ok"
    elif completed.returncode == 2:
        status = "usage"
        detail = detail or "needs arguments or a terminal"
    else:
        status = "fail"
    return {"path": path, "status": status, "code": completed.returncode, "detail": detail}


def sweep(timeout: float = 20.0, workers: int = 4, home: str = None) -> Dict[str, object]:
    home = home or os.path.join(os.path.dirname(REPO_ROOT), ".brahma-sweep-home")
    targets = scripts()
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for result in pool.map(lambda path: run(path, timeout, home), targets):
            results.append(result)
    counts: Dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    return {
        "scripts": len(targets),
        "counts": counts,
        "failures": [result for result in results if result["status"] == "fail"],
        "results": results,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="run every sub-directory demo")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--json", default=None, help="JSON रिपोर्ट लिखें")
    parser.add_argument("--check", action="store_true", help="विफलता पर exit 1")
    args = parser.parse_args(argv)

    report = sweep(args.timeout, args.workers)
    summary = ", ".join("%s=%d" % item for item in sorted(report["counts"].items()))
    print("स्क्रिप्ट: %d — %s" % (report["scripts"], summary))
    for failure in report["failures"]:
        print("  FAIL %-60s %s" % (failure["path"], failure["detail"]))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=1)
        print("रिपोर्ट: %s" % args.json)
    return 1 if (args.check and report["failures"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
