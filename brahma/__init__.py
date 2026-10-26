"""BRAHMA — a Sanskrit-native programming language and execution engine.

This package is the *canonical* implementation of the BRAHMA language core:

    brahma.lexer     -> tokens
    brahma.parser    -> abstract syntax tree
    brahma.compiler  -> versioned bytecode
    brahma.vm        -> stack virtual machine
    brahma.cli       -> command line interface (``python -m brahma``)

The historical demo scripts in the repository root (``सूत्र_*.py`` and
friends) are kept for reference only; they are documented in
``docs/AUDIT.md`` and their behaviour is pinned by
``tests/legacy_baseline.json``.

Example
-------
>>> from brahma import run_source
>>> result = run_source('दर्शय "नमस्ते"')
>>> result.ok, result.output
(True, ['नमस्ते'])
"""

from __future__ import annotations

from .errors import (
    BrahmaError,
    BytecodeError,
    CompileError,
    LexError,
    ParseError,
    RuntimeFault,
)
from .lexer import Lexer, Lexer as Tokenizer, tokenize
from .tokens import KEYWORDS, Token, TokenKind, normalize_digits
from .parser import Parser, parse
from .compiler import Compiler, compile_source, compile_file
from .vm import VM, Frame, run_code
from .bytecode import CodeObject, Instruction, OPCODES, dump_bytecode, load_bytecode
from .api import ExecutionResult, execute, run_file, run_source, disassemble

__version__ = "3.6.0"
__all__ = [
    "__version__",
    "BrahmaError",
    "BytecodeError",
    "CompileError",
    "LexError",
    "ParseError",
    "RuntimeFault",
    "Lexer",
    "Tokenizer",
    "tokenize",
    "Token",
    "TokenKind",
    "KEYWORDS",
    "normalize_digits",
    "Parser",
    "parse",
    "Compiler",
    "compile_source",
    "compile_file",
    "CodeObject",
    "Instruction",
    "OPCODES",
    "dump_bytecode",
    "load_bytecode",
    "VM",
    "Frame",
    "run_code",
    "ExecutionResult",
    "execute",
    "run_file",
    "run_source",
    "disassemble",
]
