"""The BRAHMA lexer.

Splits Sanskrit (or ASCII) source text into :class:`~brahma.tokens.Token`
objects.  The lexer understands:

* Unicode identifiers (Devanagari letters, marks, digits, ``_`` and ASCII)
* Devanagari numerals (१२३ == 123)
* integer, float and exponent literals
* single and double quoted strings with ``\\n \\t \\\\ \\" \\'`` escapes
* ``#`` line comments
* ``;`` as an optional statement separator
"""

from __future__ import annotations

import unicodedata
from typing import List, Optional

from .errors import LexError
from .tokens import KEYWORDS, OPERATORS, Token, TokenKind, normalize_digits

_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    '"': '"',
    "'": "'",
    "0": "\0",
}


def _is_identifier_start(ch: str) -> bool:
    if ch == "_":
        return True
    category = unicodedata.category(ch)
    return category.startswith("L") or category == "Nl"


def _is_identifier_part(ch: str) -> bool:
    if ch in ("_", "\u200c", "\u200d"):  # underscore, ZWNJ, ZWJ
        return True
    category = unicodedata.category(ch)
    return category.startswith(("L", "M", "N"))


class Lexer:
    """Turn source text into a list of tokens."""

    def __init__(self, source: str, source_name: str = "<input>") -> None:
        if not isinstance(source, str):
            raise TypeError("source must be str, got %r" % type(source).__name__)
        self.source = source
        self.source_name = source_name
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        #: Bracket depth: newlines inside ``()``/``[]``/``{}`` are continuations,
        #: so a literal or call may span several lines (as in every other
        #: language people actually write).
        self.depth = 0

    # -- helpers ---------------------------------------------------------
    def _peek(self, offset: int = 0) -> str:
        index = self.pos + offset
        if index < len(self.source):
            return self.source[index]
        return ""

    def _advance(self, count: int = 1) -> str:
        chunk = self.source[self.pos : self.pos + count]
        for ch in chunk:
            if ch == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        self.pos += count
        return chunk

    def _error(self, message: str, line: Optional[int] = None, column: Optional[int] = None) -> LexError:
        return LexError(
            message,
            line=self.line if line is None else line,
            column=self.column if column is None else column,
            source_name=self.source_name,
        )

    def _add(self, kind: TokenKind, value, line: int, column: int, text: str) -> None:
        self.tokens.append(Token(kind, value, line, column, text))

    # -- scanners --------------------------------------------------------
    def _scan_string(
        self,
        line: Optional[int] = None,
        column: Optional[int] = None,
        interpolated: bool = False,
    ) -> None:
        quote = self._peek()
        if line is None:
            line, column = self.line, self.column
        self._advance()
        chars: List[str] = []
        while True:
            ch = self._peek()
            if ch == "":
                raise self._error("असमाप्त शब्द (unterminated string)", line, column)
            if ch == "\n":
                raise self._error("शब्द पंक्ति में समाप्त नहीं हुआ (newline in string)", line, column)
            if ch == quote:
                self._advance()
                break
            if ch == "\\":
                self._advance()
                esc = self._peek()
                if esc == "":
                    raise self._error("अमान्य escape अनुक्रम", line, column)
                if esc in _ESCAPES:
                    chars.append(_ESCAPES[esc])
                    self._advance()
                elif esc == "u":
                    self._advance()
                    hex_digits = self.source[self.pos : self.pos + 4]
                    if len(hex_digits) != 4:
                        raise self._error("अपूर्ण \\u escape", line, column)
                    try:
                        chars.append(chr(int(hex_digits, 16)))
                    except ValueError:
                        raise self._error("अमान्य \\u escape: %r" % hex_digits, line, column)
                    self._advance(4)
                else:
                    raise self._error("अमान्य escape अनुक्रम '\\%s'" % esc, line, column)
                continue
            chars.append(ch)
            self._advance()
        prefix = "$" if interpolated else ""
        self._add(TokenKind.STRING, "".join(chars), line, column, prefix + quote + quote)

    def _scan_number(self) -> None:
        line, column = self.line, self.column
        start = self.pos
        while self._peek() and (self._peek().isdigit() or self._peek() in "०१२३४५६७८९"):
            self._advance()
        is_float = False
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            self._advance()
            while self._peek().isdigit():
                self._advance()
        if self._peek() in ("e", "E"):
            lookahead = self._peek(1)
            if lookahead.isdigit() or (lookahead in "+-" and self._peek(2).isdigit()):
                is_float = True
                self._advance()
                if self._peek() in "+-":
                    self._advance()
                while self._peek().isdigit():
                    self._advance()
        raw = self.source[start : self.pos]
        text = normalize_digits(raw)
        try:
            value = float(text) if is_float else int(text)
        except ValueError:  # pragma: no cover - defensive
            raise self._error("अमान्य संख्या %r" % raw, line, column)
        self._add(TokenKind.NUMBER, value, line, column, raw)

    def _scan_name(self) -> None:
        line, column = self.line, self.column
        start = self.pos
        while self._peek() and _is_identifier_part(self._peek()):
            self._advance()
        text = self.source[start : self.pos]
        if text in KEYWORDS:
            self._add(TokenKind.KEYWORD, KEYWORDS[text], line, column, text)
        else:
            self._add(TokenKind.NAME, text, line, column, text)

    # -- entry point -----------------------------------------------------
    def tokenize(self) -> List[Token]:
        """Return the full token list (always terminated by ``EOF``)."""
        if self.tokens:
            return list(self.tokens)
        while self.pos < len(self.source):
            ch = self._peek()
            if ch in " \t\r\f\v":
                self._advance()
                continue
            if ch == "\n":
                line, column = self.line, self.column
                self._advance()
                if self.depth == 0:
                    self._add(TokenKind.NEWLINE, "\n", line, column, "\n")
                continue
            if ch == "#":
                while self._peek() not in ("", "\n"):
                    self._advance()
                continue
            if ch == "$" and self._peek(1) in "'\"":
                line, column = self.line, self.column
                self._advance()  # the '$' marks an interpolated string
                self._scan_string(line, column, interpolated=True)
                continue
            if ch in "'\"":
                self._scan_string()
                continue
            if ch.isdigit() or ch in "०१२३४५६७८९":
                self._scan_number()
                continue
            if _is_identifier_start(ch):
                self._scan_name()
                continue
            matched = False
            for op in OPERATORS:
                if self.source.startswith(op, self.pos):
                    line, column = self.line, self.column
                    self._advance(len(op))
                    self._add(TokenKind.OP, op, line, column, op)
                    if op in ("(", "[", "{"):
                        self.depth += 1
                    elif op in (")", "]", "}"):
                        self.depth = max(0, self.depth - 1)
                    matched = True
                    break
            if matched:
                continue
            raise self._error("अमान्य चिह्न %r (U+%04X)" % (ch, ord(ch)))
        self.tokens.append(Token(TokenKind.EOF, None, self.line, self.column, ""))
        return list(self.tokens)


def tokenize(source: str, source_name: str = "<input>") -> List[Token]:
    """Convenience wrapper around :class:`Lexer`."""
    return Lexer(source, source_name).tokenize()
