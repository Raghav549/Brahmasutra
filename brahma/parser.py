"""Recursive descent parser for the BRAHMA language.

Grammar (EBNF, ``NL`` = newline, ``END`` = ``अन्त``/``end``)::

    program    := (NL | stmt)* EOF
    stmt       := let | assign | index_assign | print | if | while
                | func | return | break | continue | expr_stmt
    let        := "स्थापय" NAME "=" expr
    assign     := NAME ("=" | "+=" | "-=" | "*=" | "/=" | "%=") expr
    print      := "दर्शय" expr
    if         := "यदि" expr NL block
                  ("अन्यथायदि" expr NL block)*
                  ("अन्यथा" NL block)? END
    while      := "यावत्" expr NL block END
    func       := "कार्य" NAME "(" params ")" NL block END
    return     := "प्रत्यागमन" expr?
    expr       := or
    or         := and ("वा" and)*
    and        := equality ("च" equality)*
    equality   := comparison (("==" | "!=") comparison)*
    comparison := additive (("<" | "<=" | ">" | ">=") additive)*
    additive   := multiply (("+" | "-") multiply)*
    multiply   := unary (("*" | "/" | "%") unary)*
    unary      := ("न" | "-" | "+") unary | power
    power      := postfix ("**" unary)?
    postfix    := primary ("[" expr "]")*
    primary    := NUMBER | STRING | "सत्य" | "असत्य" | "शून्य"
                | NAME "(" args ")" | NAME | "[" items "]" | "(" expr ")"
"""

from __future__ import annotations

from typing import List, Optional

from . import ast_nodes as ast
from .errors import ParseError
from .lexer import tokenize
from .tokens import Token, TokenKind

_COMPARISONS = ("==", "!=", "<", "<=", ">", ">=")
_ASSIGN_OPS = ("=", "+=", "-=", "*=", "/=", "%=")


class Parser:
    """Turn tokens into an :class:`~brahma.ast_nodes.Program`."""

    def __init__(self, tokens: List[Token], source_name: str = "<input>") -> None:
        self.tokens = list(tokens)
        self.source_name = source_name
        self.pos = 0
        self.loop_depth = 0
        self.func_depth = 0

    # -- token helpers ---------------------------------------------------
    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        index = min(self.pos + offset, len(self.tokens) - 1)
        return self.tokens[index]

    def advance(self) -> Token:
        token = self.current
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def check(self, kind: TokenKind, value=None) -> bool:
        token = self.current
        if token.kind is not kind:
            return False
        return value is None or token.value == value

    def check_op(self, *ops: str) -> bool:
        return self.current.kind is TokenKind.OP and self.current.value in ops

    def check_keyword(self, *names: str) -> bool:
        return self.current.kind is TokenKind.KEYWORD and self.current.value in names

    def match_op(self, *ops: str) -> Optional[Token]:
        if self.check_op(*ops):
            return self.advance()
        return None

    def match_keyword(self, *names: str) -> Optional[Token]:
        if self.check_keyword(*names):
            return self.advance()
        return None

    def error(self, message: str, token: Optional[Token] = None) -> ParseError:
        token = token or self.current
        found = token.text or (token.value if token.value is not None else "अन्त")
        return ParseError(
            "%s (मिला: %r, पंक्ति %d)" % (message, found, token.line),
            line=token.line,
            column=token.column,
            source_name=self.source_name,
        )

    def expect_op(self, op: str) -> Token:
        if not self.check_op(op):
            raise self.error("'%s' अपेक्षित था" % op)
        return self.advance()

    def expect_name(self, what: str = "नाम") -> Token:
        if not self.check(TokenKind.NAME):
            raise self.error("%s अपेक्षित था" % what)
        return self.advance()

    def skip_newlines(self) -> None:
        while self.check(TokenKind.NEWLINE) or self.check_op(";"):
            self.advance()

    # -- statements ------------------------------------------------------
    def parse(self) -> ast.Program:
        statements: List[ast.Node] = []
        self.skip_newlines()
        while not self.check(TokenKind.EOF):
            statements.append(self.statement())
            self.skip_newlines()
        return ast.Program(statements=statements, line=1)

    def statement(self) -> ast.Node:
        token = self.current

        if self.match_keyword("LET"):
            name = self.expect_name("चर का नाम")
            self.expect_op("=")
            value = self.expression()
            return ast.LetStmt(line=token.line, name=name.value, value=value)

        if self.match_keyword("PRINT"):
            value = self.expression()
            return ast.PrintStmt(line=token.line, value=value)

        if self.check_keyword("IF"):
            return self.if_statement()

        if self.match_keyword("WHILE"):
            self.loop_depth += 1
            condition = self.expression()
            body = self.block()
            self.loop_depth -= 1
            return ast.WhileStmt(line=token.line, condition=condition, body=body)

        if self.match_keyword("FUNC"):
            return self.func_statement(token)

        if self.match_keyword("RETURN"):
            if self.func_depth == 0:
                raise self.error("'प्रत्यागमन' केवल कार्य के भीतर मान्य है", token)
            if self.check(TokenKind.NEWLINE) or self.check(TokenKind.EOF) or self.check_keyword("END"):
                return ast.ReturnStmt(line=token.line, value=None)
            return ast.ReturnStmt(line=token.line, value=self.expression())

        if self.match_keyword("BREAK"):
            if self.loop_depth == 0:
                raise self.error("'विराम' केवल चक्र के भीतर मान्य है", token)
            return ast.BreakStmt(line=token.line)

        if self.match_keyword("CONTINUE"):
            if self.loop_depth == 0:
                raise self.error("'चल' केवल चक्र के भीतर मान्य है", token)
            return ast.ContinueStmt(line=token.line)

        if self.check_keyword("END", "ELSE", "ELIF"):
            raise self.error("अप्रत्याशित '%s'" % token.text, token)

        return self.simple_statement()

    def simple_statement(self) -> ast.Node:
        token = self.current
        # Assignment forms: ``x = expr``, ``x += expr``, ``a[i] = expr``
        if self.check(TokenKind.NAME) and self.peek().kind is TokenKind.OP:
            nxt = self.peek().value
            if nxt in _ASSIGN_OPS:
                name = self.advance().value
                op = self.advance().value
                value = self.expression()
                return ast.AssignStmt(line=token.line, name=name, value=value, op=op)
            if nxt == "[":
                # Look ahead for ``name[...] = expr``; otherwise it is an
                # ordinary index expression statement.
                depth = 0
                index = self.pos + 1
                while index < len(self.tokens):
                    tok = self.tokens[index]
                    if tok.kind is TokenKind.OP and tok.value == "[":
                        depth += 1
                    elif tok.kind is TokenKind.OP and tok.value == "]":
                        depth -= 1
                        if depth == 0:
                            break
                    index += 1
                after = self.tokens[index + 1] if index + 1 < len(self.tokens) else None
                if after is not None and after.kind is TokenKind.OP and after.value == "=":
                    target = ast.Name(line=token.line, name=self.advance().value)
                    self.expect_op("[")
                    subscript = self.expression()
                    self.expect_op("]")
                    self.expect_op("=")
                    value = self.expression()
                    return ast.IndexAssignStmt(
                        line=token.line, target=target, index=subscript, value=value
                    )

        expr = self.expression()
        return ast.ExprStmt(line=token.line, value=expr)

    def if_statement(self) -> ast.IfStmt:
        token = self.advance()  # IF
        root = ast.IfStmt(line=token.line, condition=self.expression(), body=self.block(), orelse=[])
        current = root
        self.skip_newlines()

        while self.check_keyword("ELIF"):
            elif_token = self.advance()
            node = ast.IfStmt(
                line=elif_token.line,
                condition=self.expression(),
                body=self.block(),
                orelse=[],
            )
            current.orelse = [node]
            current = node
            self.skip_newlines()

        if self.match_keyword("ELSE"):
            current.orelse = self.block()
        return root

    def func_statement(self, token: Token) -> ast.FuncDef:
        name = self.expect_name("कार्य का नाम")
        self.expect_op("(")
        params: List[str] = []
        if not self.check_op(")"):
            while True:
                params.append(self.expect_name("पैरामीटर").value)
                if not self.match_op(","):
                    break
        self.expect_op(")")
        self.func_depth += 1
        saved_loop = self.loop_depth
        self.loop_depth = 0
        body = self.block()
        self.loop_depth = saved_loop
        self.func_depth -= 1
        return ast.FuncDef(line=token.line, name=name.value, params=params, body=body)

    def block(self) -> List[ast.Node]:
        """Parse a newline separated block terminated by ``END``."""
        self.skip_newlines()
        statements: List[ast.Node] = []
        while not self.check_keyword("END", "ELSE", "ELIF") and not self.check(TokenKind.EOF):
            statements.append(self.statement())
            self.skip_newlines()
        if self.check_keyword("END"):
            self.advance()
        elif self.check(TokenKind.EOF):
            raise self.error("'अन्त' अपेक्षित था (block अधूरा है)")
        return statements

    # -- expressions -----------------------------------------------------
    def expression(self) -> ast.Node:
        return self.logic_or()

    def logic_or(self) -> ast.Node:
        node = self.logic_and()
        while self.check_keyword("OR"):
            token = self.advance()
            right = self.logic_and()
            node = ast.BinaryOp(line=token.line, op="or", left=node, right=right)
        return node

    def logic_and(self) -> ast.Node:
        node = self.equality()
        while self.check_keyword("AND"):
            token = self.advance()
            right = self.equality()
            node = ast.BinaryOp(line=token.line, op="and", left=node, right=right)
        return node

    def equality(self) -> ast.Node:
        node = self.comparison()
        while self.check_op("==", "!="):
            token = self.advance()
            right = self.comparison()
            node = ast.Compare(line=token.line, op=token.value, left=node, right=right)
        return node

    def comparison(self) -> ast.Node:
        node = self.additive()
        while self.check_op("<", "<=", ">", ">="):
            token = self.advance()
            right = self.additive()
            node = ast.Compare(line=token.line, op=token.value, left=node, right=right)
        return node

    def additive(self) -> ast.Node:
        node = self.multiply()
        while self.check_op("+", "-"):
            token = self.advance()
            right = self.multiply()
            node = ast.BinaryOp(line=token.line, op=token.value, left=node, right=right)
        return node

    def multiply(self) -> ast.Node:
        node = self.unary()
        while self.check_op("*", "/", "%"):
            token = self.advance()
            right = self.unary()
            node = ast.BinaryOp(line=token.line, op=token.value, left=node, right=right)
        return node

    def unary(self) -> ast.Node:
        if self.check_keyword("NOT"):
            token = self.advance()
            return ast.UnaryOp(line=token.line, op="not", operand=self.unary())
        if self.check_op("-", "+"):
            token = self.advance()
            return ast.UnaryOp(line=token.line, op=token.value, operand=self.unary())
        return self.power()

    def power(self) -> ast.Node:
        node = self.postfix()
        if self.check_op("**"):
            token = self.advance()
            right = self.unary()  # right associative
            return ast.BinaryOp(line=token.line, op="**", left=node, right=right)
        return node

    def postfix(self) -> ast.Node:
        node = self.primary()
        while self.check_op("["):
            token = self.advance()
            index = self.expression()
            self.expect_op("]")
            node = ast.Index(line=token.line, target=node, index=index)
        return node

    def primary(self) -> ast.Node:
        token = self.current

        if token.kind is TokenKind.NUMBER:
            self.advance()
            return ast.Literal(line=token.line, value=token.value)

        if token.kind is TokenKind.STRING:
            self.advance()
            return ast.Literal(line=token.line, value=token.value)

        if token.kind is TokenKind.KEYWORD:
            if token.value == "TRUE":
                self.advance()
                return ast.Literal(line=token.line, value=True)
            if token.value == "FALSE":
                self.advance()
                return ast.Literal(line=token.line, value=False)
            if token.value == "NULL":
                self.advance()
                return ast.Literal(line=token.line, value=None)
            raise self.error("अभिव्यक्ति में अप्रत्याशित कीवर्ड", token)

        if token.kind is TokenKind.NAME:
            self.advance()
            if self.check_op("("):
                self.advance()
                args: List[ast.Node] = []
                if not self.check_op(")"):
                    while True:
                        args.append(self.expression())
                        if not self.match_op(","):
                            break
                self.expect_op(")")
                return ast.Call(line=token.line, callee=token.value, args=args)
            return ast.Name(line=token.line, name=token.value)

        if self.match_op("("):
            node = self.expression()
            self.expect_op(")")
            return node

        if self.match_op("["):
            items: List[ast.Node] = []
            if not self.check_op("]"):
                while True:
                    items.append(self.expression())
                    if not self.match_op(","):
                        break
            self.expect_op("]")
            return ast.ListExpr(line=token.line, items=items)

        raise self.error("अभिव्यक्ति अपेक्षित थी", token)


def parse(source: str, source_name: str = "<input>") -> ast.Program:
    """Parse source text into an AST."""
    return Parser(tokenize(source, source_name), source_name).parse()


def parse_file(path: str) -> ast.Program:
    """Parse a file into an AST."""
    with open(path, "r", encoding="utf-8") as handle:
        return parse(handle.read(), source_name=path)
