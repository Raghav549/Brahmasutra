"""High level convenience API used by tests, the CLI and embedders."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from .bytecode import CodeObject, disassemble as disassemble_code, dump_bytecode
from .compiler import compile_file as _compile_file
from .compiler import compile_source
from .errors import BrahmaError
from .vm import DEFAULT_STEP_LIMIT, VM, format_value


@dataclass
class ExecutionResult:
    """Everything that happened during one program run."""

    value: Any = None
    output: List[str] = field(default_factory=list)
    steps: int = 0
    error: Optional[BrahmaError] = None
    elapsed: float = 0.0

    @property
    def ok(self) -> bool:
        """True when the program finished without an error."""
        return self.error is None

    def stdout(self) -> str:
        """Captured output joined with newlines."""
        return "\n".join(self.output)


def execute(
    source: str,
    source_name: str = "<input>",
    out: Optional[Callable[[str], None]] = None,
    echo: bool = False,
    step_limit: int = DEFAULT_STEP_LIMIT,
    max_depth: int = 500,
) -> ExecutionResult:
    """Compile and run ``source``, capturing output and errors.

    Output is always captured on the result; if ``out`` is provided each
    line is also forwarded to it.
    """
    result = ExecutionResult()
    started = time.perf_counter()
    lines: List[str] = []

    def sink(text: str) -> None:
        lines.append(text)
        if out is not None:
            out(text)

    try:
        code = compile_source(source, source_name=source_name, echo=echo)
        vm = VM(out=sink, step_limit=step_limit, max_depth=max_depth)
        result.value = vm.run(code)
        result.steps = vm.steps
    except BrahmaError as exc:
        result.error = exc
    finally:
        result.output = lines
        result.elapsed = time.perf_counter() - started
    return result


def run_source(source: str, **kwargs: Any) -> ExecutionResult:
    """Run source text (thin alias of :func:`execute`)."""
    return execute(source, **kwargs)


def run_file(path: str, **kwargs: Any) -> ExecutionResult:
    """Read ``path`` (UTF-8) and run it."""
    with open(path, "r", encoding="utf-8") as handle:
        return execute(handle.read(), source_name=path, **kwargs)


def compile_source_to_code(source: str, source_name: str = "<input>", echo: bool = False) -> CodeObject:
    """Compile source text to a :class:`CodeObject`."""
    return compile_source(source, source_name=source_name, echo=echo)


def compile_file(path: str) -> CodeObject:
    """Compile a file to bytecode."""
    return _compile_file(path)


def disassemble(source: str, source_name: str = "<input>") -> str:
    """Compile ``source`` and return a readable bytecode listing."""
    return disassemble_code(compile_source(source, source_name=source_name))


def build_bytecode_file(source_path: str, output_path: str) -> int:
    """Compile ``source_path`` into a ``.sbc`` image; return its size."""
    code = _compile_file(source_path)
    blob = dump_bytecode(code, output_path)
    return len(blob)


def load_and_run(path: str, **kwargs: Any) -> ExecutionResult:
    """Run a compiled ``.sbc`` file."""
    from .bytecode import load_bytecode

    result = ExecutionResult()
    lines: List[str] = []
    sink_provided = kwargs.pop("out", None)

    def sink(text: str) -> None:
        lines.append(text)
        if sink_provided is not None:
            sink_provided(text)

    try:
        code = load_bytecode(path)
        vm = VM(out=sink, **kwargs)
        result.value = vm.run(code)
        result.steps = vm.steps
    except BrahmaError as exc:
        result.error = exc
    finally:
        result.output = lines
    return result


def render(result: ExecutionResult) -> str:  # pragma: no cover - convenience
    """Render a result as text (used by the CLI and notebooks)."""
    parts = list(result.output)
    if result.ok and result.value is not None:
        parts.append(format_value(result.value))
    elif result.error is not None:
        parts.append(result.error.format())
    return os.linesep.join(parts)
