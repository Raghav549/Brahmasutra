"""AST -> bytecode compiler."""

from __future__ import annotations

from typing import List, Optional, Tuple

from . import ast_nodes as ast
from .bytecode import BINARY_OPS, COMPARE_OPS, UNARY_OPS, CodeObject
from .errors import CompileError
from .parser import parse, parse_file

_COMPOUND = {"+=": "+", "-=": "-", "*=": "*", "/=": "/", "%=": "%"}


class Compiler:
    """Lower an AST into a :class:`~brahma.bytecode.CodeObject`.

    Parameters
    ----------
    echo:
        When true, the value of a bare expression statement is printed.
        This is what the REPL wants; normal programs discard such values.
    """

    def __init__(self, echo: bool = False) -> None:
        self.echo = echo
        self.loops: List[Tuple[int, List[int], List[int]]] = []
        self.function: Optional[CodeObject] = None

    # -- public API ------------------------------------------------------
    def compile(self, program: ast.Program, name: str = "<module>", source_name: str = "<input>") -> CodeObject:
        code = CodeObject(name=name, source_name=source_name)
        self._statements(program.statements, code)
        code.emit("HALT", line=program.line)
        code.validate()
        return code

    # -- helpers ---------------------------------------------------------
    def _statements(self, statements: List[ast.Node], code: CodeObject) -> None:
        for statement in statements:
            self._statement(statement, code)

    def _statement(self, node: ast.Node, code: CodeObject) -> None:
        if isinstance(node, ast.LetStmt):
            self._expr(node.value, code)
            code.emit("STORE_NAME", node.name, node.line)

        elif isinstance(node, ast.AssignStmt):
            if node.op == "=":
                self._expr(node.value, code)
            else:
                operator = _COMPOUND[node.op]
                code.emit("LOAD_NAME", node.name, node.line)
                self._expr(node.value, code)
                code.emit("BINARY", operator, node.line)
            code.emit("STORE_NAME", node.name, node.line)

        elif isinstance(node, ast.IndexAssignStmt):
            self._expr(node.target, code)
            self._expr(node.index, code)
            self._expr(node.value, code)
            code.emit("STORE_INDEX", line=node.line)

        elif isinstance(node, ast.PrintStmt):
            self._expr(node.value, code)
            code.emit("PRINT", line=node.line)

        elif isinstance(node, ast.ExprStmt):
            self._expr(node.value, code)
            code.emit("PRINT" if self.echo else "POP", line=node.line)

        elif isinstance(node, ast.IfStmt):
            self._if(node, code)

        elif isinstance(node, ast.WhileStmt):
            self._while(node, code)

        elif isinstance(node, ast.FuncDef):
            self._function(node, code)

        elif isinstance(node, ast.ReturnStmt):
            if self.function is None:
                raise CompileError("'प्रत्यागमन' कार्य के बाहर", line=node.line)
            if node.value is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.value, code)
            code.emit("RETURN", line=node.line)

        elif isinstance(node, ast.BreakStmt):
            if not self.loops:
                raise CompileError("'विराम' चक्र के बाहर", line=node.line)
            _, breaks, _ = self.loops[-1]
            breaks.append(code.emit("JUMP", None, node.line))

        elif isinstance(node, ast.ContinueStmt):
            if not self.loops:
                raise CompileError("'चल' चक्र के बाहर", line=node.line)
            start, _, continues = self.loops[-1]
            continues.append(code.emit("JUMP", start, node.line))

        else:  # pragma: no cover - defensive
            raise CompileError("अज्ञात AST नोड %r" % type(node).__name__, line=getattr(node, "line", 0))

    def _if(self, node: ast.IfStmt, code: CodeObject) -> None:
        self._expr(node.condition, code)
        jump_else = code.emit("JUMP_IF_FALSE", None, node.line)
        self._statements(node.body, code)
        if node.orelse:
            jump_end = code.emit("JUMP", None, node.line)
            code.instructions[jump_else].arg = len(code)
            self._statements(node.orelse, code)
            code.instructions[jump_end].arg = len(code)
        else:
            code.instructions[jump_else].arg = len(code)

    def _while(self, node: ast.WhileStmt, code: CodeObject) -> None:
        start = len(code)
        self._expr(node.condition, code)
        jump_out = code.emit("JUMP_IF_FALSE", None, node.line)

        self.loops.append((start, [], []))
        self._statements(node.body, code)
        _, breaks, continues = self.loops.pop()

        code.emit("JUMP", start, node.line)
        end = len(code)
        code.instructions[jump_out].arg = end
        for index in breaks:
            code.instructions[index].arg = end
        for index in continues:
            if code.instructions[index].arg is None:  # pragma: no cover - defensive
                code.instructions[index].arg = start

    def _function(self, node: ast.FuncDef, code: CodeObject) -> None:
        func_code = CodeObject(
            name=node.name,
            params=list(node.params),
            source_name=code.source_name,
        )
        previous = self.function
        saved_loops = self.loops
        self.function = func_code
        self.loops = []
        self._statements(node.body, func_code)
        func_code.emit("LOAD_CONST", None, node.line)
        func_code.emit("RETURN", line=node.line)
        self.function = previous
        self.loops = saved_loops
        func_code.validate()
        code.emit("MAKE_FUNCTION", func_code, node.line)
        code.emit("STORE_NAME", node.name, node.line)

    def _expr(self, node: ast.Node, code: CodeObject) -> None:
        if isinstance(node, ast.Literal):
            code.emit("LOAD_CONST", node.value, node.line)

        elif isinstance(node, ast.Name):
            code.emit("LOAD_NAME", node.name, node.line)

        elif isinstance(node, ast.ListExpr):
            for item in node.items:
                self._expr(item, code)
            code.emit("BUILD_LIST", len(node.items), node.line)

        elif isinstance(node, ast.Index):
            self._expr(node.target, code)
            self._expr(node.index, code)
            code.emit("LOAD_INDEX", line=node.line)

        elif isinstance(node, ast.Call):
            code.emit("LOAD_NAME", node.callee, node.line)
            for argument in node.args:
                self._expr(argument, code)
            code.emit("CALL", len(node.args), node.line)

        elif isinstance(node, ast.UnaryOp):
            self._expr(node.operand, code)
            if node.op not in UNARY_OPS:
                raise CompileError("अमान्य यूनरी ऑपरेटर %r" % node.op, line=node.line)
            code.emit("UNARY", node.op, node.line)

        elif isinstance(node, ast.BinaryOp):
            if node.op in ("and", "or"):
                self._expr(node.left, code)
                code.emit("DUP", line=node.line)
                jump = code.emit(
                    "JUMP_IF_FALSE" if node.op == "and" else "JUMP_IF_TRUE", None, node.line
                )
                code.emit("POP", line=node.line)
                self._expr(node.right, code)
                code.instructions[jump].arg = len(code)
            else:
                if node.op not in BINARY_OPS:
                    raise CompileError("अमान्य बाइनरी ऑपरेटर %r" % node.op, line=node.line)
                self._expr(node.left, code)
                self._expr(node.right, code)
                code.emit("BINARY", node.op, node.line)

        elif isinstance(node, ast.Compare):
            if node.op not in COMPARE_OPS:
                raise CompileError("अमान्य तुलना ऑपरेटर %r" % node.op, line=node.line)
            self._expr(node.left, code)
            self._expr(node.right, code)
            code.emit("COMPARE", node.op, node.line)

        else:  # pragma: no cover - defensive
            raise CompileError("अज्ञात अभिव्यक्ति %r" % type(node).__name__, line=getattr(node, "line", 0))


def compile_source(source: str, name: str = "<module>", source_name: str = "<input>", echo: bool = False) -> CodeObject:
    """Parse and compile ``source`` in one step."""
    program = parse(source, source_name)
    return Compiler(echo=echo).compile(program, name=name, source_name=source_name)


def compile_file(path: str, name: Optional[str] = None, echo: bool = False) -> CodeObject:
    """Parse and compile a ``.sutra`` source file."""
    program = parse_file(path)
    return Compiler(echo=echo).compile(program, name=name or "<module>", source_name=path)
