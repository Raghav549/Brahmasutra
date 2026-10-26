"""Compiler tests: emitted instructions, jumps and validation."""

from __future__ import annotations

import pytest

from brahma import CompileError, compile_source
from brahma.bytecode import CodeObject, Instruction, disassemble


def ops(source, **kwargs):
    return [instr.op for instr in compile_source(source, **kwargs).instructions]


class TestEmission:
    def test_literal_and_print(self):
        assert ops('दर्शय "x"') == ["LOAD_CONST", "PRINT", "HALT"]

    def test_let(self):
        assert ops("स्थापय अ = 1") == ["LOAD_CONST", "STORE_NAME", "HALT"]

    def test_expression_statement_is_popped(self):
        assert ops("1 + 2") == ["LOAD_CONST", "LOAD_CONST", "BINARY", "POP", "HALT"]

    def test_echo_mode_prints_expression_statements(self):
        assert ops("1 + 2", echo=True)[-2] == "PRINT"

    def test_if_without_else(self):
        code = compile_source("यदि सत्य\n दर्शय 1\nअन्त")
        assert "JUMP_IF_FALSE" in [i.op for i in code.instructions]
        # no trailing jump when there is no else branch
        assert [i.op for i in code.instructions].count("JUMP") == 0

    def test_if_with_else_has_two_jumps(self):
        code = compile_source('यदि सत्य\n दर्शय 1\nअन्यथा\n दर्शय 2\nअन्त')
        assert [i.op for i in code.instructions].count("JUMP") >= 1
        assert "JUMP_IF_FALSE" in [i.op for i in code.instructions]

    def test_while_has_backward_jump(self):
        code = compile_source("यावत् असत्य\n दर्शय 1\nअन्त")
        jumps = [i for i in code.instructions if i.op == "JUMP"]
        assert jumps
        assert jumps[0].arg is not None and jumps[0].arg < len(code.instructions)

    def test_break_and_continue_targets_are_patched(self):
        source = (
            "यावत् सत्य\n"
            " विराम\n"
            " चल\n"
            "अन्त"
        )
        code = compile_source(source)
        targets = [i.arg for i in code.instructions if i.op == "JUMP"]
        assert all(isinstance(t, int) for t in targets)
        assert all(0 <= t <= len(code.instructions) for t in targets)

    def test_short_circuit_emits_conditional_jump(self):
        code = compile_source("अ = 1 च 2")
        names = [i.op for i in code.instructions]
        assert "DUP" in names
        assert "JUMP_IF_FALSE" in names

    def test_or_uses_jump_if_true(self):
        code = compile_source("अ = 1 वा 2")
        assert "JUMP_IF_TRUE" in [i.op for i in code.instructions]

    def test_function_definition(self):
        code = compile_source("कार्य f(a)\n प्रत्यागमन a\nअन्त")
        make = [i for i in code.instructions if i.op == "MAKE_FUNCTION"]
        assert len(make) == 1
        nested = make[0].arg
        assert isinstance(nested, CodeObject)
        assert nested.params == ["a"]
        assert nested.instructions[-1].op == "RETURN"

    def test_function_without_explicit_return_returns_null(self):
        code = compile_source("कार्य f()\n दर्शय 1\nअन्त")
        nested = [i for i in code.instructions if i.op == "MAKE_FUNCTION"][0].arg
        assert nested.instructions[-2].op == "LOAD_CONST"
        assert nested.instructions[-2].arg is None
        assert nested.instructions[-1].op == "RETURN"

    def test_list_literal(self):
        code = compile_source("दर्शय [1, 2, 3]")
        assert code.instructions[3].op == "BUILD_LIST"
        assert code.instructions[3].arg == 3

    def test_index_assignment(self):
        names = ops("स[0] = 1")
        assert names[:5] == ["LOAD_NAME", "LOAD_CONST", "LOAD_CONST", "STORE_INDEX", "HALT"]

    def test_compound_assignment_loads_first(self):
        names = ops("अ += 1")
        assert names[0] == "LOAD_NAME"
        assert "BINARY" in names

    def test_module_source_name_is_recorded(self):
        code = compile_source("दर्शय 1", source_name="demo.sutra")
        assert code.source_name == "demo.sutra"

    def test_halt_is_last(self):
        code = compile_source("दर्शय 1")
        assert code.instructions[-1].op == "HALT"


class TestValidation:
    def test_code_object_validate_rejects_bad_jump(self):
        code = CodeObject(name="f")
        code.emit("JUMP", 99)
        with pytest.raises(Exception) as info:
            code.validate()
        assert "जम्प" in str(info.value)

    def test_invalid_opcode(self):
        with pytest.raises(Exception):
            Instruction(op="NOT_AN_OP")

    def test_invalid_binary_operator(self):
        code = CodeObject(name="f")
        code.emit("BINARY", "??")
        with pytest.raises(Exception):
            code.validate()

    def test_compiler_rejects_unknown_operator(self):
        # Constructed by hand to hit the defensive branch.
        from brahma import ast_nodes as ast
        from brahma import Compiler

        compiler = Compiler()
        code = CodeObject(name="f")
        node = ast.BinaryOp(line=1, op="?", left=ast.Literal(line=1, value=1), right=ast.Literal(line=1, value=2))
        with pytest.raises(CompileError):
            compiler._expr(node, code)


class TestDisassembly:
    def test_contains_function_names(self):
        text = disassemble(compile_source("कार्य जोड़(a, b)\n प्रत्यागमन a + b\nअन्त"))
        assert "कार्य" not in text  # opcodes are ASCII
        assert "MAKE_FUNCTION" in text
        assert "जोड़" in text

    def test_lists_instruction_indices(self):
        text = disassemble(compile_source("दर्शय 1"))
        assert "LOAD_CONST" in text
        assert "0" in text
