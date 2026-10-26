"""Token definitions and the Sanskrit/English keyword table."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Dict


class TokenKind(str, enum.Enum):
    """The lexical categories produced by :class:`brahma.lexer.Lexer`."""

    NUMBER = "NUMBER"
    STRING = "STRING"
    NAME = "NAME"
    KEYWORD = "KEYWORD"
    OP = "OP"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


#: Sanskrit keywords mapped to canonical English names, including ASCII
#: aliases so that programmers who do not read Devanagari can still write
#: BRAHMA code.
KEYWORDS: Dict[str, str] = {
    # control flow
    "यदि": "IF",
    "if": "IF",
    "अन्यथा": "ELSE",
    "else": "ELSE",
    "अन्यथायदि": "ELIF",
    "elif": "ELIF",
    "यावत्": "WHILE",
    "while": "WHILE",
    "अन्त": "END",
    "end": "END",
    "विराम": "BREAK",
    "break": "BREAK",
    "चल": "CONTINUE",
    "continue": "CONTINUE",
    # functions
    "कार्य": "FUNC",
    "func": "FUNC",
    "def": "FUNC",
    "प्रत्यागमन": "RETURN",
    "return": "RETURN",
    # binding
    "स्थापय": "LET",
    "let": "LET",
    # printing / IO
    "दर्शय": "PRINT",
    "print": "PRINT",
    # literals
    "सत्य": "TRUE",
    "true": "TRUE",
    "असत्य": "FALSE",
    "false": "FALSE",
    "शून्य": "NULL",
    "null": "NULL",
    "none": "NULL",
    # boolean operators
    "च": "AND",
    "and": "AND",
    "वा": "OR",
    "or": "OR",
    "न": "NOT",
    "not": "NOT",
}

#: Two character operators must be matched before single character ones.
OPERATORS = (
    "**",
    "==",
    "!=",
    "<=",
    ">=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ",",
    ":",
    ";",
    "+",
    "-",
    "*",
    "/",
    "%",
    "<",
    ">",
    "=",
)

#: Devanagari digits U+0966 .. U+096F and their ASCII equivalents.
DEVANAGARI_DIGITS = {chr(0x0966 + i): str(i) for i in range(10)}


@dataclass(frozen=True)
class Token:
    """A single lexical unit.

    ``value`` holds the decoded value for numbers/strings and the *canonical*
    keyword name for keywords.  ``text`` holds the raw source text.
    """

    kind: TokenKind
    value: Any
    line: int
    column: int
    text: str = ""

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return "Token(%s, %r, %d:%d)" % (self.kind.value, self.value, self.line, self.column)


def normalize_digits(text: str) -> str:
    """Translate Devanagari digits to ASCII digits."""
    return "".join(DEVANAGARI_DIGITS.get(ch, ch) for ch in text)
