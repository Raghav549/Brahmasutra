"""Virtual machine tests: semantics, builtins and runtime diagnostics."""

from __future__ import annotations

import pytest

from brahma import VM
from brahma.api import execute


def out(source, **kwargs):
    result = execute(source, **kwargs)
    assert result.ok, result.error.format() if result.error else ""
    return result.output


def error_of(source, **kwargs):
    result = execute(source, **kwargs)
    assert not result.ok, "expected failure, got output: %r" % (result.output,)
    return result.error


class TestArithmetic:
    def test_addition(self):
        assert out("दर्शय 2 + 3") == ["5"]

    def test_precedence(self):
        assert out("दर्शय 2 + 3 * 4") == ["14"]

    def test_parentheses(self):
        assert out("दर्शय (2 + 3) * 4") == ["20"]

    def test_subtraction_and_negation(self):
        assert out("दर्शय 10 - 4 - 3") == ["3"]
        assert out("दर्शय -5 + 2") == ["-3"]

    def test_true_division(self):
        assert out("दर्शय 7 / 2") == ["3.5"]

    def test_integer_division_result_is_float(self):
        assert out("दर्शय 20 / 10") == ["2.0"]

    def test_modulo(self):
        assert out("दर्शय 7 % 3") == ["1"]

    def test_power(self):
        assert out("दर्शय 2 ** 10") == ["1024"]

    def test_power_right_associative(self):
        assert out("दर्शय 2 ** 3 ** 2") == ["512"]

    def test_division_by_zero(self):
        fault = error_of("दर्शय 1 / 0")
        assert "शून्य" in fault.message

    def test_modulo_by_zero(self):
        fault = error_of("दर्शय 1 % 0")
        assert "शून्य" in fault.message

    def test_type_error_addition(self):
        fault = error_of('दर्शय 1 + "a"')
        assert "संख्या" in fault.message

    def test_boolean_arithmetic_is_rejected(self):
        fault = error_of("दर्शय सत्य + 1")
        assert "बूलियन" in fault.message


class TestStrings:
    def test_concatenation(self):
        assert out('दर्शय "नम" + "स्ते"') == ["नमस्ते"]

    def test_repetition(self):
        assert out('दर्शय "ab" * 3') == ["ababab"]

    def test_index(self):
        assert out('दर्शय "सूत्र"[1]') == ["ू"]

    def test_negative_index(self):
        assert out('दर्शय "abc"[-1]') == ["c"]

    def test_index_out_of_range(self):
        fault = error_of('दर्शय "abc"[9]')
        assert "सीमा" in fault.message

    def test_non_integer_index(self):
        fault = error_of('दर्शय "abc"["x"]')
        assert "पूर्णांक" in fault.message

    def test_comparison(self):
        assert out('दर्शय "क" < "ख"') == ["सत्य"]


class TestVariables:
    def test_let_and_use(self):
        assert out("स्थापय अ = 10\nदर्शय अ") == ["10"]

    def test_reassignment(self):
        assert out("अ = 1\nअ = 2\nदर्शय अ") == ["2"]

    def test_compound_assignment(self):
        assert out("अ = 10\nअ += 5\nदर्शय अ") == ["15"]

    def test_underscore_and_unicode_names(self):
        assert out("स्थापय कर्म_संख्या = 7\nदर्शय कर्म_संख्या") == ["7"]

    def test_undefined_name(self):
        fault = error_of("दर्शय अज्ञात")
        assert "अपरिभाषित" in fault.message
        assert fault.line == 1

    def test_error_includes_source_name(self):
        result = execute("दर्शय अज्ञात", source_name="demo.sutra")
        assert "demo.sutra" in result.error.format()


class TestControlFlow:
    def test_if_true(self):
        assert out('यदि सत्य\n दर्शय "हाँ"\nअन्त') == ["हाँ"]

    def test_if_false(self):
        assert out('यदि असत्य\n दर्शय "हाँ"\nअन्त') == []

    def test_if_else(self):
        assert out('यदि असत्य\n दर्शय 1\nअन्यथा\n दर्शय 2\nअन्त') == ["2"]

    def test_elif_chain(self):
        source = (
            "अ = 2\n"
            "यदि अ == 1\n"
            ' दर्शय "एक"\n'
            "अन्यथायदि अ == 2\n"
            ' दर्शय "दो"\n'
            "अन्यथा\n"
            ' दर्शय "अन्य"\n'
            "अन्त"
        )
        assert out(source) == ["दो"]

    def test_truthiness_of_zero_and_empty(self):
        assert out('यदि 0\n दर्शय "सत्य"\nअन्यथा\n दर्शय "असत्य"\nअन्त') == ["असत्य"]
        assert out('यदि ""\n दर्शय "सत्य"\nअन्यथा\n दर्शय "असत्य"\nअन्त') == ["असत्य"]

    def test_while_loop(self):
        source = "i = 0\nयावत् i < 3\n दर्शय i\n i = i + 1\nअन्त"
        assert out(source) == ["0", "1", "2"]

    def test_break(self):
        source = "i = 0\nयावत् सत्य\n i = i + 1\n यदि i == 3\n  विराम\n अन्त\nअन्त\nदर्शय i"
        assert out(source) == ["3"]

    def test_continue(self):
        source = (
            "i = 0\n"
            "यावत् i < 5\n"
            " i = i + 1\n"
            " यदि i % 2 == 0\n"
            "  चल\n"
            " अन्त\n"
            " दर्शय i\n"
            "अन्त"
        )
        assert out(source) == ["1", "3", "5"]

    def test_nested_loops(self):
        source = (
            "i = 0\n"
            "यावत् i < 2\n"
            " j = 0\n"
            " यावत् j < 2\n"
            "  दर्शय i * 10 + j\n"
            "  j = j + 1\n"
            " अन्त\n"
            " i = i + 1\n"
            "अन्त"
        )
        assert out(source) == ["0", "1", "10", "11"]


class TestLogic:
    def test_and_or(self):
        assert out("दर्शय सत्य च असत्य") == ["असत्य"]
        assert out("दर्शय असत्य वा सत्य") == ["सत्य"]

    def test_not(self):
        assert out("दर्शय न असत्य") == ["सत्य"]

    def test_short_circuit_and(self):
        # The right operand is undefined but must never be evaluated.
        assert out("दर्शय असत्य च अज्ञात") == ["असत्य"]

    def test_short_circuit_or(self):
        assert out("दर्शय सत्य वा अज्ञात") == ["सत्य"]

    def test_and_returns_operand_value(self):
        assert out("दर्शय 0 च 5") == ["0"]
        assert out("दर्शय 2 च 5") == ["5"]

    def test_comparisons(self):
        assert out("दर्शय 1 < 2") == ["सत्य"]
        assert out("दर्शय 2 <= 2") == ["सत्य"]
        assert out("दर्शय 3 > 4") == ["असत्य"]
        assert out("दर्शय 3 >= 3") == ["सत्य"]

    def test_equality_between_types_is_false(self):
        assert out('दर्शय 1 == "1"') == ["असत्य"]

    def test_numeric_equality_across_int_float(self):
        assert out("दर्शय 1 == 1.0") == ["सत्य"]

    def test_bool_is_not_a_number(self):
        assert out("दर्शय सत्य == 1") == ["असत्य"]

    def test_ordered_comparison_between_types_fails(self):
        fault = error_of('दर्शय 1 < "2"')
        assert "तुलना" in fault.message


class TestFunctions:
    def test_simple_call(self):
        source = "कार्य योग(क, ख)\n प्रत्यागमन क + ख\nअन्त\nदर्शय योग(3, 4)"
        assert out(source) == ["7"]

    def test_no_argument_function(self):
        source = "कार्य नमस्ते()\n प्रत्यागमन 42\nअन्त\nदर्शय नमस्ते()"
        assert out(source) == ["42"]

    def test_implicit_none_return(self):
        source = "कार्य f()\n दर्शय 1\nअन्त\nदर्शय f()"
        assert out(source) == ["1", "शून्य"]

    def test_recursion(self):
        source = (
            "कार्य फिब(n)\n"
            " यदि n < 2\n"
            "  प्रत्यागमन n\n"
            " अन्त\n"
            " प्रत्यागमन फिब(n - 1) + फिब(n - 2)\n"
            "अन्त\n"
            "दर्शय फिब(15)"
        )
        assert out(source) == ["610"]

    def test_mutual_recursion_style_nested_calls(self):
        source = (
            "कार्य दुगुना(x)\n प्रत्यागमन x * 2\nअन्त\n"
            "कार्य चौगुना(x)\n प्रत्यागमन दुगुना(दुगुना(x))\nअन्त\n"
            "दर्शय चौगुना(3)"
        )
        assert out(source) == ["12"]

    def test_early_return_inside_loop(self):
        source = (
            "कार्य खोज(n)\n"
            " i = 0\n"
            " यावत् i < 10\n"
            "  यदि i == n\n"
            "   प्रत्यागमन i * 100\n"
            "  अन्त\n"
            "  i = i + 1\n"
            " अन्त\n"
            " प्रत्यागमन -1\n"
            "अन्त\n"
            "दर्शय खोज(3)"
        )
        assert out(source) == ["300"]

    def test_wrong_argument_count(self):
        fault = error_of("कार्य f(a)\n प्रत्यागमन a\nअन्त\nf(1, 2)")
        assert "आर्ग्युमेंट" in fault.message

    def test_calling_a_number_fails(self):
        fault = error_of("अ = 5\nअ()")
        assert "आह्वान" in fault.message

    def test_function_sees_globals(self):
        assert out("अ = 10\nकार्य f()\n प्रत्यागमन अ + 1\nअन्त\nदर्शय f()") == ["11"]

    def test_function_locals_do_not_leak(self):
        source = "कार्य f()\n अ = 1\n प्रत्यागमन अ\nअन्त\nf()\nदर्शय अ"
        fault = error_of(source)
        assert "अपरिभाषित" in fault.message

    def test_argument_shadows_global(self):
        source = "x = 1\nकार्य f(x)\n प्रत्यागमन x\nअन्त\nदर्शय f(9)\nदर्शय x"
        assert out(source) == ["9", "1"]

    def test_recursion_depth_limit(self):
        source = "कार्य f()\n प्रत्यागमन f()\nअन्त\nf()"
        fault = error_of(source)
        assert "गहराई" in fault.message


class TestLists:
    def test_literal_and_print(self):
        assert out("दर्शय [1, 2, 3]") == ["[1, 2, 3]"]

    def test_index(self):
        assert out("स = [10, 20]\nदर्शय स[1]") == ["20"]

    def test_negative_index(self):
        assert out("स = [10, 20]\nदर्शय स[-1]") == ["20"]

    def test_index_assignment(self):
        assert out("स = [1, 2]\nस[0] = 9\nदर्शय स") == ["[9, 2]"]

    def test_index_out_of_range(self):
        fault = error_of("स = [1]\nदर्शय स[5]")
        assert "सीमा" in fault.message

    def test_store_index_on_string_fails(self):
        fault = error_of('स = "abc"\nस[0] = "x"')
        assert "सूची" in fault.message

    def test_list_concatenation(self):
        assert out("दर्शय [1] + [2]") == ["[1, 2]"]

    def test_nested_list(self):
        assert out("दर्शय [[1], [2, 3]]") == ["[[1], [2, 3]]"]


class TestBuiltins:
    def test_len(self):
        assert out('दर्शय लम्बाई("abc")') == ["3"]
        assert out("दर्शय लम्बाई([1, 2])") == ["2"]

    def test_len_wrong_type(self):
        fault = error_of("दर्शय लम्बाई(5)")
        assert "लम्बाई" in fault.message

    def test_int_and_str(self):
        assert out('दर्शय संख्या("42") + 1') == ["43"]
        assert out("दर्शय पाठ(42)") == ["42"]

    def test_int_invalid(self):
        fault = error_of('दर्शय संख्या("नमस्ते")')
        assert "संख्या" in fault.message

    def test_float(self):
        assert out('दर्शय दशमलव("2.5") * 2') == ["5.0"]

    def test_abs_min_max(self):
        assert out("दर्शय निरपेक्ष(-3)") == ["3"]
        assert out("दर्शय न्यूनतम(3, 1, 2)") == ["1"]
        assert out("दर्शय अधिकतम([4, 9, 2])") == ["9"]

    def test_range(self):
        assert out("दर्शय श्रेणी(3)") == ["[0, 1, 2]"]

    def test_range_indexing(self):
        assert out("स = श्रेणी(3)\nदर्शय स[2]") == ["2"]

    def test_join(self):
        assert out('दर्शय जोड़ो("-", ["a", "b"])') == ["a-b"]

    def test_append_returns_list(self):
        assert out('स = [1]\nजोड़ें(स, 2)\nदर्शय स') == ["[1, 2]"]

    def test_builtin_arity(self):
        fault = error_of("दर्शय लम्बाई()")
        assert "आर्ग्युमेंट" in fault.message

    def test_ascii_builtin_aliases(self):
        assert out("दर्शय len([1, 2, 3])") == ["3"]

    def test_print_builtin_writes_to_out(self):
        assert out('print("x")') == ["x"]


class TestFormatting:
    def test_none(self):
        assert out("दर्शय शून्य") == ["शून्य"]

    def test_booleans(self):
        assert out("दर्शय सत्य\nदर्शय असत्य") == ["सत्य", "असत्य"]

    def test_float_whole_number(self):
        assert out("दर्शय 4.0") == ["4.0"]

    def test_string_is_not_quoted(self):
        assert out('दर्शय "abc"') == ["abc"]

    def test_multiple_prints(self):
        assert out("दर्शय 1\nदर्शय 2") == ["1", "2"]


class TestLimits:
    def test_step_limit(self):
        source = "यावत् सत्य\n i = 1\nअन्त"
        result = execute(source, step_limit=50)
        assert not result.ok
        assert "चरण सीमा" in result.error.message

    def test_step_limit_zero(self):
        result = execute("दर्शय 1", step_limit=0)
        assert not result.ok

    def test_output_is_captured_even_on_error(self):
        result = execute("दर्शय 1\nदर्शय 1 / 0")
        assert result.output == ["1"]
        assert not result.ok

    def test_vm_requires_code_object(self):
        with pytest.raises(TypeError):
            VM().run("not code")

    def test_out_none_discards_output(self):
        result = execute("दर्शय 1", out=None)
        assert result.output == ["1"]

    def test_traceback_contains_function_names(self):
        source = (
            "कार्य आन्तरिक()\n दर्शय 1 / 0\nअन्त\n"
            "कार्य बाहरी()\n आन्तरिक()\nअन्त\n"
            "बाहरी()"
        )
        fault = error_of(source)
        names = [name for name, _ in fault.frames]
        assert "बाहरी" in names
        assert "आन्तरिक" in names
        assert "आन्तरिक" in fault.traceback_text()


class TestTablesAndSlices:
    """Dictionaries, slicing and the extended standard library (2.x → 3.0)."""

    def test_dict_literal_and_indexing(self):
        result = execute('स्थापय त = {"नाम": "ब्रह्म", "संख्या": 3}\nदर्शय त["नाम"]\nदर्शय त["संख्या"]')
        assert result.output == ["ब्रह्म", "3"]

    def test_dict_assignment_and_nested_update(self):
        source = (
            'स्थापय त = {"सूची": [1, 2]}\n'
            'त["सूची"][1] = 9\n'
            'त["नया"] = 4\n'
            'दर्शय त["सूची"][1] + त["नया"]'
        )
        assert execute(source).output == ["13"]

    def test_missing_key_is_a_runtime_fault(self):
        fault = error_of('स्थापय त = {}\nदर्शय त["नहीं"]')
        assert "कुंजी" in str(fault)

    def test_slices_on_lists_and_strings(self):
        source = (
            "स्थापय स = [10, 20, 30, 40]\n"
            "दर्शय स[1:3]\nदर्शय स[:2]\nदर्शय स[2:]\n"
            'दर्शय "सूत्र"[1:3]'
        )
        assert execute(source).output == ["[20, 30]", "[10, 20]", "[30, 40]", "ूत"]

    def test_dict_and_list_builtins(self):
        source = (
            'स्थापय त = तालिका()\n'
            'त["क"] = 1\nत["ख"] = 2\n'
            "दर्शय कुंजियाँ(त)\n"
            'दर्शय समाविष्ट(त, "क")\n'
            'दर्शय हटाओ_कुंजी(त, "क")\n'
            "दर्शय योगफल([1, 2, 3])\n"
            "दर्शय क्रम([3, 1, 2])\n"
            "दर्शय उलटा([1, 2, 3])\n"
            "दर्शय गिनती([1, 1, 2], 1)\n"
            "दर्शय हटाओ([1, 2, 3])\n"
            "दर्शय सम्मिलित([1, 3], 1, 2)\n"
            "दर्शय विस्तार([1], [2, 3])"
        )
        assert execute(source).output == [
            "[क, ख]", "सत्य", "1", "6", "[1, 2, 3]", "[3, 2, 1]", "2", "3",
            "[1, 2, 3]", "[1, 2, 3]",
        ]

    def test_string_builtins(self):
        source = (
            'दर्शय विभाजन("a,b,c", ",")\n'
            'दर्शय प्रतिस्थापन("सूत्र-OS", "-", " ")\n'
            'दर्शय त्रिम("  ॐ  ")\n'
            'दर्शय बड़े("om")\n'
            'दर्शय खोज("सूत्र", "त्")\n'
            'दर्शय दोहराओ("ॐ", 3)'
        )
        assert execute(source).output == ["[a, b, c]", "सूत्र OS", "ॐ", "OM", "2", "ॐॐॐ"]

    def test_program_may_span_lines_inside_brackets(self):
        source = (
            'स्थापय त = {\n  "क": 1,\n  "ख": 2\n}\n'
            "दर्शय योगफल(मान(त))\n"
            "स्थापय स = [\n 10,\n 20\n]\nदर्शय स[1]"
        )
        assert execute(source).output == ["3", "20"]

    def test_type_builtin_reports_real_types(self):
        source = (
            'दर्शय प्रकार(1) + "/" + प्रकार(1.5) + "/" + प्रकार("x") + "/" '
            '+ प्रकार([1]) + "/" + प्रकार({}) + "/" + प्रकार(सत्य)'
        )
        assert execute(source).output == ["पूर्णांक/दशमलव/शब्द/सूची/तालिका/बूलियन"]
