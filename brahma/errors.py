"""Error types raised by the BRAHMA toolchain.

Every error carries an optional source position (``line`` / ``column``) and
an optional ``source_name`` so that the CLI can print compiler-style
diagnostics such as::

    demo.सूत्र:4:11: त्रुटि: अपरिभाषित नाम 'अ'
"""

from __future__ import annotations

from typing import Optional


class BrahmaError(Exception):
    """Base class for all BRAHMA errors."""

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source_name: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.source_name = source_name

    def format(self) -> str:
        """Return a human readable, single line diagnostic."""
        where = ""
        if self.line is not None:
            where = "%s:%d" % (self.source_name or "<input>", self.line)
            if self.column is not None:
                where += ":%d" % self.column
            where += ": "
        return where + self.message

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.format()


class LexError(BrahmaError):
    """Raised when the source cannot be split into tokens."""


class ParseError(BrahmaError):
    """Raised when the token stream does not form a valid program."""


class CompileError(BrahmaError):
    """Raised when an AST cannot be lowered to bytecode."""


class BytecodeError(BrahmaError):
    """Raised when a bytecode file is malformed or from a newer format."""


class RuntimeFault(BrahmaError):
    """Raised when a program fails while executing.

    ``frames`` holds the call stack (innermost last) as
    ``(function_name, line)`` tuples.
    """

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source_name: Optional[str] = None,
        frames: Optional[list] = None,
        catchable: bool = True,
    ) -> None:
        super().__init__(message, line=line, column=column, source_name=source_name)
        self.frames = list(frames or [])
        #: ``False`` for guard-rail faults (step budget, call depth) that a
        #: ``प्रयास``/``पकड़`` block must not be able to swallow.
        self.catchable = catchable

    def traceback_text(self) -> str:
        """Render a compact stack trace."""
        lines = []
        for name, line in self.frames:
            lines.append("  %s में (पंक्ति %s)" % (name, line))
        if not lines:
            return ""
        return "आह्वान शृंखला:\n" + "\n".join(lines)
