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
        self.loops: List[Tuple[int, List[int], List[int], int]] = []
        #: ``अन्ततः`` blocks in scope, innermost last.  ``विराम``, ``चल`` and
        #: ``प्रत्यागमन`` must run them before leaving the guard.
        self.exits: List[List[ast.Node]] = []
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
        if isinstance(node, ast.ImportStmt):
            code.emit("IMPORT", [node.path, node.alias or ""], node.line)

        elif isinstance(node, ast.LetStmt):
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

        elif isinstance(node, ast.TryStmt):
            self._try(node, code)

        elif isinstance(node, ast.ScopeDecl):
            for name in node.names:
                code.emit("DECLARE_NONLOCAL" if node.kind == "nonlocal"
                          else "DECLARE_GLOBAL", name, node.line)

        elif isinstance(node, ast.RaiseStmt):
            if node.value is None:
                code.emit("LOAD_CONST", "उठाया गया अपवाद", node.line)
            else:
                self._expr(node.value, code)
            code.emit("RAISE", line=node.line)

        elif isinstance(node, ast.SliceAssignStmt):
            self._expr(node.target, code)
            if node.start is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.start, code)
            if node.stop is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.stop, code)
            self._expr(node.value, code)
            code.emit("STORE_SLICE", line=node.line)

        elif isinstance(node, ast.ReturnStmt):
            if self.function is None:
                raise CompileError("'प्रत्यागमन' कार्य के बाहर", line=node.line)
            if node.value is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.value, code)
            # The return value waits on the stack: every statement is
            # stack-balanced, so it is still on top when RETURN runs.
            self._run_exits(code, 0, node.line)
            code.emit("RETURN", line=node.line)

        elif isinstance(node, ast.BreakStmt):
            if not self.loops:
                raise CompileError("'विराम' चक्र के बाहर", line=node.line)
            _, breaks, _, depth = self.loops[-1]
            self._run_exits(code, depth, node.line)
            breaks.append(code.emit("JUMP", None, node.line))

        elif isinstance(node, ast.ContinueStmt):
            if not self.loops:
                raise CompileError("'चल' चक्र के बाहर", line=node.line)
            start, _, continues, depth = self.loops[-1]
            self._run_exits(code, depth, node.line)
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

        self.loops.append((start, [], [], len(self.exits)))
        self._statements(node.body, code)
        _, breaks, continues, _ = self.loops.pop()

        code.emit("JUMP", start, node.line)
        end = len(code)
        code.instructions[jump_out].arg = end
        for index in breaks:
            code.instructions[index].arg = end
        for index in continues:
            if code.instructions[index].arg is None:  # pragma: no cover - defensive
                code.instructions[index].arg = start

    @staticmethod
    def _split_declarations(statements: List[ast.Node]):
        """Pull top-level ``बाह्य``/``वैश्विक`` declarations out of a body."""
        body: List[ast.Node] = []
        declarations = []
        for statement in statements:
            if isinstance(statement, ast.ScopeDecl):
                declarations.extend((statement.kind, name) for name in statement.names)
            else:
                body.append(statement)
        return body, declarations

    def _run_exits(self, code: CodeObject, depth: int, line: int) -> None:
        """Inline every ``अन्ततः`` body from the innermost down to ``depth``.

        Compiling an exit block temporarily trims the stack so that a
        ``प्रत्यागमन`` *inside* a ``अन्ततः`` runs the remaining outer blocks
        instead of recursing into itself.
        """
        for index in range(len(self.exits) - 1, depth - 1, -1):
            saved = self.exits
            self.exits = saved[:index]
            try:
                self._statements(saved[index], code)
            finally:
                self.exits = saved

    def _try(self, node: ast.TryStmt, code: CodeObject) -> None:
        """``प्रयास`` … ``पकड़`` … ``अन्ततः`` … — a real handler table.

        ``अन्ततः`` bodies are inlined on every exit path (normal completion,
        handler completion, and each ``प्रत्यागमन``/``विराम``/``चल`` inside the
        guard), so the block runs exactly once however control leaves.
        """
        has_final = bool(node.final)
        if has_final:
            self.exits.append(node.final)

        guard = code.emit("TRY", [0, node.name], node.line)
        self._statements(node.body, code)
        code.emit("END_TRY", line=node.line)
        if has_final:
            self.exits.pop()
            self._statements(node.final, code)
        jump_end = code.emit("JUMP", None, node.line)

        code.instructions[guard].arg[0] = len(code)
        if node.handler:
            inner = None
            if has_final:
                self.exits.append(node.final)
                inner = code.emit("TRY", [0, node.name], node.line)
            self._statements(node.handler, code)
            if has_final:
                self.exits.pop()
                code.emit("END_TRY", line=node.line)
                self._statements(node.final, code)
                jump_done = code.emit("JUMP", None, node.line)
                code.instructions[inner].arg[0] = len(code)
                self._statements(node.final, code)
                code.emit("RERAISE", line=node.line)
                code.instructions[jump_done].arg = len(code)
            code.instructions[jump_end].arg = len(code)
            return

        # No handler: run ``अन्ततः`` and let the fault keep propagating.
        self._statements(node.final, code)
        code.emit("RERAISE", line=node.line)
        code.instructions[jump_end].arg = len(code)

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
        body, declarations = self._split_declarations(node.body)
        for kind, name in declarations:
            func_code.emit("DECLARE_NONLOCAL" if kind == "nonlocal" else "DECLARE_GLOBAL",
                           name, node.line)
        self._statements(body, func_code)
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

        elif isinstance(node, ast.TupleExpr):
            for item in node.items:
                self._expr(item, code)
            code.emit("BUILD_TUPLE", len(node.items), node.line)

        elif isinstance(node, ast.DictExpr):
            for key, value in zip(node.keys, node.values):
                self._expr(key, code)
                self._expr(value, code)
            code.emit("BUILD_DICT", len(node.keys), node.line)

        elif isinstance(node, ast.Index):
            self._expr(node.target, code)
            self._expr(node.index, code)
            code.emit("LOAD_INDEX", line=node.line)

        elif isinstance(node, ast.Slice):
            self._expr(node.target, code)
            if node.start is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.start, code)
            if node.stop is None:
                code.emit("LOAD_CONST", None, node.line)
            else:
                self._expr(node.stop, code)
            code.emit("LOAD_SLICE", line=node.line)

        elif isinstance(node, ast.Call):
            if node.target is not None:
                self._expr(node.target, code)
            else:
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
