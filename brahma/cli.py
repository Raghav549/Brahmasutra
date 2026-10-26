"""Command line interface: ``python -m brahma ...``.

Commands::

    brahma run      FILE.sutra [--limit N] [--quiet]
    brahma compile  FILE.sutra [-o FILE.sbc]
    brahma disasm   FILE.sutra|FILE.sbc
    brahma check    FILE.sutra
    brahma repl
    brahma modules [NAME]     मानक पुस्तकालय के मॉड्यूल
    brahma llm SUBCOMMAND …   (देखें: python -m brahma llm --help)
    brahma version

Exit codes: ``0`` success, ``1`` program error, ``2`` usage error.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from . import __version__
from .api import build_bytecode_file, disassemble, execute, load_and_run
from .bytecode import load_bytecode, disassemble as disassemble_code
from .compiler import compile_file
from .errors import BrahmaError, ParseError
from .vm import DEFAULT_STEP_LIMIT, VM


def _read_source(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def _report_error(error: BrahmaError, stream=None) -> None:
    stream = stream or sys.stderr
    stream.write("त्रुटि: %s\n" % error.format())
    frames = getattr(error, "frames", None)
    if frames:
        stream.write("आह्वान शृंखला:\n")
        for name, line in frames:
            stream.write("  %s में (पंक्ति %s)\n" % (name, line))


def cmd_run(args: argparse.Namespace) -> int:
    source = _read_source(args.file)
    result = execute(
        source,
        source_name=args.file,
        out=None if args.quiet else (lambda text: print(text)),
        step_limit=args.limit,
    )
    if not result.ok:
        _report_error(result.error)
        return 1
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    output = args.output or (os.path.splitext(args.file)[0] + ".sbc")
    try:
        size = build_bytecode_file(args.file, output)
    except BrahmaError as error:
        _report_error(error)
        return 1
    print("संकलित: %s (%d बाइट)" % (output, size))
    return 0


def cmd_disasm(args: argparse.Namespace) -> int:
    try:
        if args.file.endswith(".sbc"):
            print(disassemble_code(load_bytecode(args.file)))
        else:
            print(disassemble(_read_source(args.file), args.file))
    except BrahmaError as error:
        _report_error(error)
        return 1
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    try:
        compile_file(args.file)
    except BrahmaError as error:
        _report_error(error)
        return 1
    print("ठीक: %s" % args.file)
    return 0


def cmd_run_bytecode(args: argparse.Namespace) -> int:
    result = load_and_run(args.file, out=lambda text: print(text), step_limit=args.limit)
    if not result.ok:
        _report_error(result.error)
        return 1
    return 0


class Repl:
    """A small read-eval-print loop that keeps globals between lines."""

    def __init__(self, out=None, step_limit: int = DEFAULT_STEP_LIMIT) -> None:
        self.out = out or (lambda text: print(text))
        self.vm = VM(out=self.out, step_limit=step_limit)
        self.buffer: List[str] = []

    def evaluate(self, source: str):
        from .compiler import compile_source

        code = compile_source(source, source_name="<repl>", echo=True)
        return self.vm.run(code)

    def handle(self, line: str) -> bool:
        """Process one input line; return False to leave the REPL."""
        stripped = line.strip()
        if stripped in (":quit", ":exit", "exit", "निर्गम"):
            return False
        if not stripped:
            return True
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        try:
            self.evaluate(source)
            self.buffer = []
        except ParseError as error:
            if "अन्त" in error.message and "अपेक्षित" in error.message:
                return True  # keep reading a block
            print("त्रुटि: %s" % error.format(), file=sys.stderr)
            self.buffer = []
        except BrahmaError as error:
            _report_error(error)
            self.buffer = []
        return True


def cmd_repl(args: argparse.Namespace) -> int:
    print("BRAHMA %s — सूत्र REPL (बाहर निकलने के लिए :quit)" % __version__)
    repl = Repl(step_limit=args.limit)
    while True:
        prompt = "सूत्र >>> " if not repl.buffer else "      ... "
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not repl.handle(line):
            return 0


def cmd_modules(args: argparse.Namespace) -> int:
    """List the ``.सूत्र`` standard library, or show one module's exports."""
    vm = VM(out=None)
    if not args.name:
        found = {}
        for root in vm.stdlib_dirs():
            if not os.path.isdir(root):
                continue
            for entry in sorted(os.listdir(root)):
                if entry.endswith((".सूत्र", ".sutra")) and entry not in found:
                    found[entry] = root
        if not found:
            print("कोई मानक मॉड्यूल नहीं मिला")
            return 0
        for entry, root in sorted(found.items()):
            print("%-24s %s" % (entry, root))
        return 0
    try:
        exports = vm.load_module(args.name)
    except BrahmaError as error:
        _report_error(error)
        return 1
    print("%s — %d नाम" % (args.name, len(exports)))
    for name in sorted(exports):
        print("  %s" % name)
    return 0


def cmd_llm(args: argparse.Namespace) -> int:
    """Delegate ``brahma llm ...`` to :mod:`brahma_llm.cli`."""
    rest = list(args.rest or [])
    if rest and rest[0] == "--":
        rest = rest[1:]
    try:
        from brahma_llm.cli import main as llm_main
    except ImportError:
        sys.stderr.write("त्रुटि: brahma_llm उपलब्ध नहीं (रिपॉज़िटरी रूट से चलाएँ)\n")
        return 1
    return int(llm_main(rest))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brahma",
        description="BRAHMA — संस्कृत-आधारित प्रोग्रामिंग भाषा",
    )
    parser.add_argument("--version", action="version", version="BRAHMA %s" % __version__)
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="स्रोत चलाएँ")
    run.add_argument("file")
    run.add_argument("--limit", type=int, default=DEFAULT_STEP_LIMIT, help="अधिकतम चरण")
    run.add_argument("--quiet", action="store_true", help="आउटपुट न दिखाएँ")
    run.set_defaults(func=cmd_run)

    compile_cmd = sub.add_parser("compile", help="बाइटकोड बनाएँ")
    compile_cmd.add_argument("file")
    compile_cmd.add_argument("-o", "--output")
    compile_cmd.set_defaults(func=cmd_compile)

    disasm = sub.add_parser("disasm", help="बाइटकोड दिखाएँ")
    disasm.add_argument("file")
    disasm.set_defaults(func=cmd_disasm)

    check = sub.add_parser("check", help="केवल वाक्यविन्यास जाँचें")
    check.add_argument("file")
    check.set_defaults(func=cmd_check)

    runbc = sub.add_parser("run-bytecode", help=".sbc फ़ाइल चलाएँ")
    runbc.add_argument("file")
    runbc.add_argument("--limit", type=int, default=DEFAULT_STEP_LIMIT)
    runbc.set_defaults(func=cmd_run_bytecode)

    repl = sub.add_parser("repl", help="इंटरैक्टिव शेल")
    repl.add_argument("--limit", type=int, default=DEFAULT_STEP_LIMIT)
    repl.set_defaults(func=cmd_repl)

    modules = sub.add_parser("modules", help="मानक पुस्तकालय के मॉड्यूल")
    modules.add_argument("name", nargs="?", help="मॉड्यूल का नाम (जैसे गणित)")
    modules.set_defaults(func=cmd_modules)

    llm = sub.add_parser("llm", help="ब्रह्म-LLM (प्रशिक्षण, लक्ष्य, आत्म-संपादन)")
    llm.add_argument("rest", nargs=argparse.REMAINDER,
                     help="उप-आदेश: info/train/generate/autotrain/evolve/kernel/...")
    llm.set_defaults(func=cmd_llm)

    version = sub.add_parser("version", help="संस्करण दिखाएँ")
    version.set_defaults(func=lambda args: (print("BRAHMA %s" % __version__), 0)[1])

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    try:
        return int(args.func(args))
    except FileNotFoundError as error:
        sys.stderr.write("त्रुटि: फ़ाइल नहीं मिली: %s\n" % error.filename)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
