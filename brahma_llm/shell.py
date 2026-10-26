"""सूत्र-OS शेल — a command line whose dispatcher is a सूत्र program.

The shell is not a Python switch statement pretending to be an OS: the kernel
image is booted once, its globals (memory allocator, process table, scheduler,
syscall table, filesystem, interrupt counters) stay live, and every command is
fed to ``शेल_चलाओ`` — a function **written in सूत्र** inside
``brahma_llm/os_kernel.py``.  Python only owns the read-eval-print loop and the
``run`` command, which compiles a सूत्र line against the same VM so that user
code executes inside the kernel's namespace.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from brahma.bytecode import CodeObject, load_bytecode
from brahma.compiler import compile_source
from brahma.errors import BrahmaError
from brahma.vm import VM

from .kernel import KERNEL_NAME, build_image, unpack_image

PROMPT = "सूत्र-OS> "

#: ``run``/``चलाओ`` prefix: compiled by the host, executed in the kernel VM.
_RUN_PREFIXES = ("run ", "चलाओ ")


class KernelShell:
    """Boot the shipped kernel and dispatch lines through its own shell."""

    def __init__(
        self,
        image: Optional[bytes] = None,
        step_limit: int = 500_000,
        writer: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.lines: List[str] = []
        self.writer = writer
        self.vm = VM(out=self.lines.append, step_limit=step_limit)
        _version, blob = unpack_image(build_image() if image is None else image)
        self.boot_value = self._execute(load_bytecode(blob), globals_seed=None)
        self.boot_output = list(self.lines)
        self._dispatch = compile_source(
            "__परिणाम = शेल_चलाओ(__पंक्ति)\n", source_name="<shell-dispatch>"
        )
        self.exited = False

    # -- execution --------------------------------------------------------
    def _execute(self, code: CodeObject, globals_seed: Optional[Dict[str, Any]] = None) -> Any:
        if globals_seed:
            self.vm.globals.update(globals_seed)
        return self.vm.run(code)

    def _capture(self, code: CodeObject, seed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        before = len(self.lines)
        ok = True
        message = ""
        value = None
        try:
            value = self._execute(code, seed)
        except BrahmaError as fault:
            ok = False
            message = fault.format()
            self.lines.append("  त्रुटि: " + message)
        output = self.lines[before:]
        if self.writer is not None:
            for line in output:
                self.writer(line)
        return {"output": output, "ok": ok, "error": message or None,
                "steps": self.vm.steps, "value": value}

    # -- public API -------------------------------------------------------
    def command(self, line: str) -> Dict[str, Any]:
        """Run one command line; returns ``output``, ``ok``, ``steps``, ``exit``."""
        text = line.strip()
        result: Dict[str, Any] = {"line": line, "output": [], "ok": True,
                                  "error": None, "steps": 0, "exit": False}
        if not text:
            return result

        for prefix in _RUN_PREFIXES:
            if text.startswith(prefix):
                source = text[len(prefix):].strip()
                if not source:
                    result.update(ok=False, error="run को सूत्र पंक्ति चाहिए",
                                  output=["  उपयोग: run <सूत्र>"])
                    return result
                try:
                    code = compile_source(source + "\n", source_name="<shell-run>")
                except BrahmaError as fault:
                    result.update(ok=False, error=fault.format(),
                                  output=["  त्रुटि: " + fault.format()])
                    return result
                result.update(self._capture(code))
                return result

        if not hasattr(self, "_dispatch"):
            result.update(ok=False, error="शेल उपलब्ध नहीं (kernel boot विफल)")
            return result
        result.update(self._capture(self._dispatch, {"__पंक्ति": text}))
        result["exit"] = self.vm.globals.get("__परिणाम") is False
        if result["exit"]:
            self.exited = True
        return result

    def script(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Feed several lines, stopping at ``exit``."""
        results = []
        for line in lines:
            result = self.command(line)
            results.append(result)
            if result["exit"]:
                break
        return results

    def repl(self, reader: Callable[[str], str] = input,
             writer: Callable[[str], None] = print) -> int:
        """Interactive loop; returns an exit status."""
        writer("%s — %d बाइट image, %d पंक्ति बूट-लॉग" % (
            KERNEL_NAME, len(build_image()), len(self.boot_output)))
        for line in self.boot_output:
            writer(line)
        writer("`help` से आदेश देखें, `exit` से बाहर।")
        while True:
            try:
                line = reader(PROMPT)
            except (EOFError, KeyboardInterrupt):
                writer("")
                return 0
            if line is None:
                return 0
            for output in self.command(line)["output"]:
                writer(output)
            if self.exited:
                return 0


def main(argv: Optional[List[str]] = None) -> int:
    """``brahma llm shell`` entry point."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        prog="brahma llm shell", description="सूत्र-OS शेल (kernel itself dispatches)"
    )
    parser.add_argument("--command", "-c", action="append", default=[],
                        help="एक आदेश चलाएँ (कई बार दिया जा सकता है)")
    parser.add_argument("--script", default=None, help="आदेश-पंक्तियों की फ़ाइल")
    parser.add_argument("--json", action="store_true", help="JSON रिपोर्ट")
    parser.add_argument("--quiet", action="store_true", help="बूट-लॉग छिपाएँ")
    args = parser.parse_args(argv)

    shell = KernelShell(writer=None if args.json else print)
    if not args.quiet and not args.json:
        print("%s — %d बाइट image" % (KERNEL_NAME, len(build_image())))
        for line in shell.boot_output:
            print(line)

    lines: List[str] = list(args.command)
    if args.script:
        with open(args.script, "r", encoding="utf-8") as handle:
            lines.extend(handle.read().splitlines())

    if lines:
        results = shell.script(lines)
        if args.json:
            print(json.dumps({"commands": results}, ensure_ascii=False, indent=1, default=str))
        return 0 if all(result["ok"] for result in results) else 1

    if args.json:
        print(json.dumps({"boot": shell.boot_output}, ensure_ascii=False, indent=1))
        return 0
    return shell.repl()


if __name__ == "__main__":  # pragma: no cover - manual entry
    raise SystemExit(main())
