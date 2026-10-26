"""Parser tests: tree shape, precedence and diagnostics."""

from __future__ import annotations

import pytest

from brahma import ParseError, parse
from brahma import ast_nodes as ast


def first(source):
    return parse(source).statements[0]


class TestStatements:
    def test_empty_program(self):
        assert parse("").statements == []

    def test_print(self):
        node = first('दर्शय "नमस्ते"')
        assert isinstance(node, ast.PrintStmt)
        assert isinstance(node.value, ast.Literal)
        assert node.value.value == "नमस्ते"

    def test_let(self):
        node = first("स्थापय अ = 1")
        assert isinstance(node, ast.LetStmt)
        assert node.name == "अ"
        assert node.value.value == 1

    def test_assignment(self):
        node = first("अ = 1")
        assert isinstance(node, ast.AssignStmt)
        assert node.op == "="

    def test_compound_assignment(self):
        node = first("अ += 2")
        assert isinstance(node, ast.AssignStmt)
        assert node.op == "+="

    def test_index_assignment(self):
        node = first("स[0] = 5")
        assert isinstance(node, ast.IndexAssignStmt)
        assert isinstance(node.target, ast.Name)

    def test_index_expression_is_not_assignment(self):
        node = first("स[0]")
        assert isinstance(node, ast.ExprStmt)
        assert isinstance(node.value, ast.Index)

    def test_semicolons_separate_statements(self):
        program = parse("अ = 1; ब = 2")
        assert len(program.statements) == 2

    def test_blank_lines_are_skipped(self):
        program = parse("\n\nअ = 1\n\n")
        assert len(program.statements) == 1

    def test_comments_only(self):
        assert parse("# कुछ नहीं\n\n").statements == []


class TestPrecedence:
    def test_multiplication_before_addition(self):
        node = first("1 + 2 * 3")
        assert isinstance(node.value, ast.BinaryOp)
        assert node.value.op == "+"
        assert node.value.right.op == "*"

    def test_parentheses_override(self):
        node = first("(1 + 2) * 3")
        assert node.value.op == "*"
        assert node.value.left.op == "+"

    def test_power_is_right_associative(self):
        node = first("2 ** 3 ** 2")
        assert node.value.op == "**"
        assert node.value.right.op == "**"

    def test_unary_minus(self):
        node = first("-5")
        assert isinstance(node.value, ast.UnaryOp)
        assert node.value.op == "-"

    def test_not(self):
        node = first("न सत्य")
        assert isinstance(node.value, ast.UnaryOp)
        assert node.value.op == "not"

    def test_comparison_lower_than_arithmetic(self):
        node = first("1 + 2 < 4")
        assert isinstance(node.value, ast.Compare)
        assert node.value.left.op == "+"

    def test_and_binds_tighter_than_or(self):
        node = first("सत्य वा असत्य च सत्य")
        assert node.value.op == "or"
        assert node.value.right.op == "and"

    def test_equality_chain(self):
        node = first("1 == 2 == 3")
        assert node.value.op == "=="
        assert node.value.left.op == "=="

    def test_call_arguments(self):
        node = first("योग(1, 2, 3)")
        assert isinstance(node.value, ast.Call)
        assert node.value.callee == "योग"
        assert len(node.value.args) == 3

    def test_nested_call(self):
        node = first("योग(गुणा(2, 3), 4)")
        assert isinstance(node.value.args[0], ast.Call)


class TestBlocks:
    def test_if_else(self):
        node = first('यदि सत्य\n दर्शय "हाँ"\nअन्यथा\n दर्शय "नहीं"\nअन्त')
        assert isinstance(node, ast.IfStmt)
        assert len(node.body) == 1
        assert len(node.orelse) == 1

    def test_if_elif_else_chain(self):
        source = (
            "यदि अ == 1\n"
            ' दर्शय "एक"\n'
            "अन्यथायदि अ == 2\n"
            ' दर्शय "दो"\n'
            "अन्यथा\n"
            ' दर्शय "अन्य"\n'
            "अन्त"
        )
        node = first(source)
        assert isinstance(node, ast.IfStmt)
        assert isinstance(node.orelse[0], ast.IfStmt)
        assert node.orelse[0].orelse[0].__class__ is ast.PrintStmt

    def test_if_without_else(self):
        node = first("यदि सत्य\n दर्शय 1\nअन्त")
        assert node.orelse == []

    def test_while(self):
        node = first("यावत् असत्य\n दर्शय 1\nअन्त")
        assert isinstance(node, ast.WhileStmt)
        assert len(node.body) == 1

    def test_nested_blocks(self):
        source = "यावत् सत्य\n यदि सत्य\n  दर्शय 1\n अन्त\nअन्त"
        node = first(source)
        assert isinstance(node.body[0], ast.IfStmt)

    def test_function_definition(self):
        node = first("कार्य योग(क, ख)\n प्रत्यागमन क + ख\nअन्त")
        assert isinstance(node, ast.FuncDef)
        assert node.params == ["क", "ख"]
        assert isinstance(node.body[0], ast.ReturnStmt)

    def test_function_no_params(self):
        node = first("कार्य नमस्ते()\n दर्शय 1\nअन्त")
        assert node.params == []


class TestErrors:
    def test_missing_end(self):
        with pytest.raises(ParseError) as info:
            parse("यदि सत्य\n दर्शय 1")
        assert "अन्त" in info.value.message

    def test_unexpected_else(self):
        with pytest.raises(ParseError) as info:
            parse("अन्यथा\n दर्शय 1\nअन्त")
        assert "अप्रत्याशित" in info.value.message

    def test_break_outside_loop(self):
        with pytest.raises(ParseError) as info:
            parse("विराम")
        assert "चक्र" in info.value.message

    def test_continue_outside_loop(self):
        with pytest.raises(ParseError):
            parse("चल")

    def test_return_outside_function(self):
        with pytest.raises(ParseError) as info:
            parse("प्रत्यागमन 1")
        assert "कार्य" in info.value.message

    def test_missing_closing_paren(self):
        with pytest.raises(ParseError):
            parse("दर्शय योग(1, 2")

    def test_missing_expression(self):
        with pytest.raises(ParseError):
            parse("दर्शय +")

    def test_error_reports_line(self):
        with pytest.raises(ParseError) as info:
            parse("अ = 1\nब = ", source_name="x.sutra")
        assert info.value.line == 2
        assert "x.sutra" in info.value.format()

    def test_incomplete_source_inside_block(self):
        with pytest.raises(ParseError):
            parse("कार्य f()\n प्रत्यागमन 1\n")
