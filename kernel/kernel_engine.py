#!/usr/bin/env python3
"""🕉️ सूत्र-OS शेल — the userland of the project's own kernel.

The old file called ``exec(code, {}, memory)`` on whatever path it was given,
which is an arbitrary-code-execution hole wearing a shell costume.  This
version is a real shell for the real OS:

``boot`` / ``verify``
    boot the ``SUTRAOS`` image built by :mod:`brahma_llm.kernel` (compiled सूत्र
    bytecode) and show the boot log; ``verify`` also enforces the boot contract
    (banner → self-test → ``READY``).
``run FILE``
    execute a ``.sutra`` program on the project's VM — the file is *compiled*,
    never ``exec``-ed as Python.
``memory``
    show the VM's global namespace after the last program.
``help`` / ``exit``
    trivial, but present so the shell is not a lie.

Non-interactive use: ``python kernel/kernel_engine.py boot`` runs one command and
exits, so scripts and CI never hang on ``input()``.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from brahma.api import execute  # noqa: E402

HELP = """सूत्र-OS शेल
  boot           कर्नेल बूट करें
  verify         बूट + स्व-परीक्षण सत्यापन
  run FILE.sutra सूत्र कार्यक्रम चलाएँ
  memory         VM की अंतिम स्थिति
  help           यह सहायता
  exit           बाहर
"""


class सूत्रKernel:
    """A shell over the सूत्र VM and the ``SUTRAOS`` boot image."""

    def __init__(self, out=None):
        self.out = out or (lambda line: print(line))
        self.running = False
        self.memory = {}
        self.processes = []
        self.last_output = []

    # -- OS --------------------------------------------------------------
    def boot(self) -> int:
        from brahma_llm.kernel import boot as boot_image

        report = boot_image()
        for line in report["output"]:
            self.out(line)
        self.memory["kernel"] = {"steps": report["steps"], "image_bytes": report["image_bytes"]}
        return 0 if report["ready"] else 1

    def verify(self) -> int:
        from brahma_llm.kernel import verify as verify_image

        report = verify_image()
        for line in report["output"]:
            self.out(line)
        if report["problems"]:
            self.out("समस्या: " + "; ".join(report["problems"]))
        else:
            self.out("कर्नेल ठीक")
        return 0 if report["ok"] else 1

    # -- userland --------------------------------------------------------
    def execute(self, path: str) -> int:
        """Compile and run a सूत्र program (no ``exec``, no Python evaluation)."""
        if not os.path.exists(path):
            self.out("फ़ाइल नहीं मिली: %s" % path)
            return 1
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        result = execute(source, source_name=path)
        self.last_output = list(result.output)
        for line in result.output:
            self.out(line)
        self.processes.append({"file": path, "ok": result.error is None, "steps": result.steps})
        if result.error is not None:
            self.out("त्रुटि: %s" % result.error.format())
            return 1
        return 0

    def show_memory(self) -> None:
        if not self.memory:
            self.out("स्मृति रिक्त")
        for key, value in self.memory.items():
            self.out("%s = %s" % (key, value))

    # -- REPL ------------------------------------------------------------
    def command(self, line: str) -> int:
        line = (line or "").strip()
        if not line:
            return 0
        if line in ("exit", "निर्गम", "quit"):
            self.running = False
            self.out("सूत्र-OS समाप्त")
            return 0
        if line in ("help", "सहायता"):
            self.out(HELP.rstrip())
            return 0
        if line in ("boot", "बूट"):
            return self.boot()
        if line in ("verify", "जाँच"):
            return self.verify()
        if line in ("memory", "स्मृति"):
            self.show_memory()
            return 0
        if line.startswith(("run ", "चलाओ ")):
            return self.execute(line.split(" ", 1)[1].strip())
        self.out("अज्ञात आदेश: %s (help देखें)" % line)
        return 1

    def loop(self) -> int:
        self.running = True
        while self.running:
            try:
                line = input("सूत्र> ")
            except (EOFError, KeyboardInterrupt):
                self.out("")
                return 0
            self.command(line)
        return 0

    def प्रारम्भ(self) -> int:
        self.out("🕉️ सूत्र-OS शेल — कर्नेल बूट हो रहा है")
        self.boot()
        return self.loop()


def मुख्य(argv=None) -> int:
    """Entry point: one command, or a REPL when no argument is given."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    kernel = सूत्रKernel()
    if arguments:
        return kernel.command(" ".join(arguments))
    return kernel.प्रारम्भ()


def _main() -> int:
    return मुख्य()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        raise SystemExit(_main())
    else:
        raise SystemExit(_brahma_cli_run(मुख्य))
