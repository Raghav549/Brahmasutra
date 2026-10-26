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


class TestClosures:
    """``कार्य`` captures its defining scope, not just the globals (3.1)."""

    def test_inner_function_reads_outer_local(self):
        source = (
            "कार्य वृद्धि(n)\n"
            "    कार्य जोड़(x)\n"
            "        प्रत्यागमन x + n\n"
            "    अन्त\n"
            "    प्रत्यागमन जोड़\n"
            "अन्त\n"
            "जोड़ो = वृद्धि(10)\n"
            "दर्शय जोड़ो(5)\n"
        )
        assert out(source) == ["15"]

    def test_two_closures_are_independent(self):
        source = (
            "कार्य गुणक(n)\n"
            "    कार्य गुणा(x)\n"
            "        प्रत्यागमन x * n\n"
            "    अन्त\n"
            "    प्रत्यागमन गुणा\n"
            "अन्त\n"
            "दो = गुणक(2)\n"
            "तीन = गुणक(3)\n"
            "दर्शय दो(7)\n"
            "दर्शय तीन(7)\n"
        )
        assert out(source) == ["14", "21"]

    def test_closure_sees_later_assignment_to_captured_name(self):
        source = (
            "कार्य बनाओ()\n"
            "    गिनती = 1\n"
            "    कार्य पढ़ो()\n"
            "        प्रत्यागमन गिनती\n"
            "    अन्त\n"
            "    गिनती = 41\n"
            "    प्रत्यागमन पढ़ो\n"
            "अन्त\n"
            "f = बनाओ()\n"
            "दर्शय f()\n"
        )
        assert out(source) == ["41"]

    def test_recursion_is_unaffected(self):
        source = (
            "कार्य क्रमगुणित(n)\n"
            "    यदि n <= 1\n"
            "        प्रत्यागमन 1\n"
            "    अन्त\n"
            "    प्रत्यागमन n * क्रमगुणित(n - 1)\n"
            "अन्त\n"
            "दर्शय क्रमगुणित(5)\n"
        )
        assert out(source) == ["120"]

    def test_globals_remain_visible(self):
        source = (
            "मान = 9\n"
            "कार्य पढ़ो()\n"
            "    प्रत्यागमन मान\n"
            "अन्त\n"
            "दर्शय पढ़ो()\n"
        )
        assert out(source) == ["9"]


class TestTryCatch:
    """``प्रयास`` / ``पकड़`` — real handlers, real unwinding (3.1)."""

    def test_division_fault_is_caught(self):
        source = (
            "प्रयास\n"
            "    दर्शय 1 / 0\n"
            "पकड़ त\n"
            "    दर्शय \"पकड़ा: \" + त\n"
            "अन्त\n"
        )
        assert out(source) == ["पकड़ा: शून्य से भाग दिया गया"]

    def test_execution_continues_after_the_handler(self):
        source = (
            "प्रयास\n"
            "    दर्शय 1 / 0\n"
            "पकड़ त\n"
            "    दर्शय \"त्रुटि\"\n"
            "अन्त\n"
            "दर्शय \"जीवित\"\n"
        )
        assert out(source) == ["त्रुटि", "जीवित"]

    def test_undefined_name_is_caught(self):
        source = (
            "प्रयास\n"
            "    दर्शय अपरिभाषित\n"
            "पकड़ गलती\n"
            "    दर्शय गलती\n"
            "अन्त\n"
        )
        assert out(source)[0].startswith("अपरिभाषित नाम")

    def test_no_fault_means_the_handler_is_skipped(self):
        source = (
            "प्रयास\n"
            "    दर्शय \"ठीक\"\n"
            "पकड़ त\n"
            "    दर्शय \"नहीं\"\n"
            "अन्त\n"
        )
        assert out(source) == ["ठीक"]

    def test_return_inside_try_returns(self):
        source = (
            "कार्य सुरक्षित(a, b)\n"
            "    प्रयास\n"
            "        प्रत्यागमन a / b\n"
            "    पकड़ त\n"
            "        प्रत्यागमन \"त्रुटि: \" + त\n"
            "    अन्त\n"
            "अन्त\n"
            "दर्शय सुरक्षित(10, 2)\n"
            "दर्शय सुरक्षित(1, 0)\n"
        )
        assert out(source) == ["5.0", "त्रुटि: शून्य से भाग दिया गया"]

    def test_fault_in_a_called_function_is_caught_by_the_caller(self):
        source = (
            "कार्य विफल()\n"
            "    प्रत्यागमन 1 / 0\n"
            "अन्त\n"
            "प्रयास\n"
            "    विफल()\n"
            "पकड़ त\n"
            "    दर्शय \"पकड़ा\"\n"
            "अन्त\n"
        )
        assert out(source) == ["पकड़ा"]

    def test_inner_handler_wins(self):
        source = (
            "प्रयास\n"
            "    प्रयास\n"
            "        दर्शय 1 / 0\n"
            "    पकड़ भीतरी\n"
            "        दर्शय \"भीतरी\"\n"
            "    अन्त\n"
            "पकड़ बाहरी\n"
            "    दर्शय \"बाहरी\"\n"
            "अन्त\n"
        )
        assert out(source) == ["भीतरी"]

    def test_uncaught_fault_still_reports(self):
        error = error_of("प्रयास\n    दर्शय 1 / 0\nपकड़ त\n    दर्शय \"ठीक\"\nअन्त\nदर्शय 1 / 0\n")
        assert "शून्य से भाग" in error.message

    def test_step_budget_cannot_be_swallowed(self):
        source = (
            "प्रयास\n"
            "    यावत् सत्य\n"
            "        x = 1\n"
            "    अन्त\n"
            "पकड़ त\n"
            "    दर्शय \"पकड़ा\"\n"
            "अन्त\n"
        )
        error = error_of(source, step_limit=500)
        assert "चरण सीमा" in error.message

    def test_bytecode_round_trip_keeps_handlers(self, tmp_path):
        from brahma import compile_source, dump_bytecode, load_bytecode
        from brahma.vm import VM

        source = "प्रयास\n    दर्शय 1 / 0\nपकड़ त\n    दर्शय \"पकड़ा\"\nअन्त\n"
        path = str(tmp_path / "try.sbc")
        dump_bytecode(compile_source(source), path)
        lines = []
        VM(out=lines.append).run(load_bytecode(path))
        assert lines == ["पकड़ा"]


class TestStringInterpolation:
    """``$"…{expr}…"`` compiles to a ``+`` chain over ``पाठ()`` (3.1)."""

    def test_variable_interpolation(self):
        assert out('नाम = "ब्रह्म"\nदर्शय $"नमस्ते {नाम}!"') == ["नमस्ते ब्रह्म!"]

    def test_expression_interpolation(self):
        assert out('दर्शय $"योग = {2 + 3}"') == ["योग = 5"]

    def test_several_placeholders(self):
        assert out('a = 1\nb = 2\nदर्शय $"{a} + {b} = {a + b}"') == ["1 + 2 = 3"]

    def test_numbers_and_lists_are_formatted(self):
        assert out('दर्शय $"सूची {[1, 2]}"') == ["सूची [1, 2]"]

    def test_escaped_braces_are_literal(self):
        assert out('दर्शय $"ब्रेस {{लिटरल}}"') == ["ब्रेस {लिटरल}"]

    def test_plain_strings_keep_their_braces(self):
        assert out('दर्शय "{अक्षुण्ण}"') == ["{अक्षुण्ण}"]

    def test_unclosed_placeholder_is_a_parse_error(self):
        error = error_of('दर्शय $"अधूरा {नाम"')
        assert "अधूरा" in error.message

    def test_embedded_syntax_error_is_reported(self):
        error = error_of('दर्शय $"त्रुटि {1 +}"')
        assert error.line == 1

    def test_interpolation_inside_a_function_and_a_call(self):
        source = (
            "कार्य अभिवादन(नाम)\n"
            "    प्रत्यागमन $\"नमस्ते {नाम}\"\n"
            "अन्त\n"
            "दर्शय अभिवादन(\"ब्रह्म\")\n"
        )
        assert out(source) == ["नमस्ते ब्रह्म"]


class TestRaiseAndFinally:
    """``उठाओ`` and ``अन्ततः`` — the other half of exception handling (3.2)."""

    def test_raise_is_caught_with_its_message(self):
        source = (
            "प्रयास\n"
            "    उठाओ \"स्वयं उठाया\"\n"
            "पकड़ त\n"
            "    दर्शय त\n"
            "अन्त\n"
        )
        assert out(source) == ["स्वयं उठाया"]

    def test_raise_takes_an_expression(self):
        source = (
            "n = -2\n"
            "प्रयास\n"
            "    उठाओ $\"ऋणात्मक: {n}\"\n"
            "पकड़ त\n"
            "    दर्शय त\n"
            "अन्त\n"
        )
        assert out(source) == ["ऋणात्मक: -2"]

    def test_uncaught_raise_reports_a_fault(self):
        error = error_of("उठाओ \"अकेला\"\n")
        assert error.message == "अकेला"
        assert error.line == 1

    def test_raise_without_a_value_uses_a_default_message(self):
        assert out("प्रयास\n    उठाओ\nपकड़ त\n    दर्शय त\nअन्त\n") == ["उठाया गया अपवाद"]

    def test_finally_runs_on_normal_completion(self):
        assert out("प्रयास\n    दर्शय \"निकाय\"\nअन्ततः\n    दर्शय \"अन्ततः\"\nअन्त\n") == \
            ["निकाय", "अन्ततः"]

    def test_finally_runs_before_the_handler_returns(self):
        source = (
            "कार्य f()\n"
            "    प्रयास\n"
            "        उठाओ \"x\"\n"
            "    पकड़ त\n"
            "        प्रत्यागमन \"पकड़ा\"\n"
            "    अन्ततः\n"
            "        दर्शय \"सफाई\"\n"
            "    अन्त\n"
            "अन्त\n"
            "दर्शय f()\n"
        )
        assert out(source) == ["सफाई", "पकड़ा"]

    def test_finally_runs_when_the_guard_returns(self):
        source = (
            "कार्य f()\n"
            "    प्रयास\n"
            "        प्रत्यागमन \"मान\"\n"
            "    अन्ततः\n"
            "        दर्शय \"सफाई\"\n"
            "    अन्त\n"
            "अन्त\n"
            "दर्शय f()\n"
        )
        assert out(source) == ["सफाई", "मान"]

    def test_finally_runs_on_break_and_continue(self):
        source = (
            "i = 0\n"
            "यावत् i < 3\n"
            "    प्रयास\n"
            "        i = i + 1\n"
            "        यदि i == 2\n"
            "            चल\n"
            "        अन्त\n"
            "        यदि i == 3\n"
            "            विराम\n"
            "        अन्त\n"
            "    अन्ततः\n"
            "        दर्शय $\"अन्ततः {i}\"\n"
            "    अन्त\n"
            "अन्त\n"
        )
        assert out(source) == ["अन्ततः 1", "अन्ततः 2", "अन्ततः 3"]

    def test_try_without_catch_runs_finally_and_re_raises(self):
        source = "प्रयास\n    उठाओ \"फिर से\"\nअन्ततः\n    दर्शय \"सफाई\"\nअन्त\n"
        error = error_of(source)
        assert error.message == "फिर से"

    def test_reraise_from_a_handler_reaches_the_outer_block(self):
        source = (
            "प्रयास\n"
            "    प्रयास\n"
            "        उठाओ \"भीतरी\"\n"
            "    पकड़ त\n"
            "        उठाओ \"पुनः: \" + त\n"
            "    अन्ततः\n"
            "        दर्शय \"भीतरी अन्ततः\"\n"
            "    अन्त\n"
            "पकड़ बाहरी\n"
            "    दर्शय बाहरी\n"
            "अन्त\n"
        )
        assert out(source) == ["भीतरी अन्ततः", "पुनः: भीतरी"]

    def test_finally_runs_once_when_the_handler_itself_raises(self):
        source = (
            "प्रयास\n"
            "    प्रयास\n"
            "        उठाओ \"पहला\"\n"
            "    पकड़ त\n"
            "        उठाओ \"दूसरा\"\n"
            "    अन्ततः\n"
            "        दर्शय \"सफाई\"\n"
            "    अन्त\n"
            "पकड़ बाहरी\n"
            "    दर्शय बाहरी\n"
            "अन्त\n"
        )
        assert out(source) == ["सफाई", "दूसरा"]

    def test_try_needs_catch_or_finally(self):
        error = error_of("प्रयास\n    दर्शय 1\nअन्त\n")
        assert "पकड़" in error.message or "अन्ततः" in error.message


class TestSliceAssignment:
    """``x[a:b] = [...]`` — the last missing lvalue form (3.2)."""

    def test_replaces_a_range(self):
        assert out("स = [1, 2, 3, 4]\nस[1:3] = [9, 9]\nदर्शय स") == ["[1, 9, 9, 4]"]

    def test_can_change_the_length(self):
        assert out("स = [1, 2, 3]\nस[1:2] = [7, 8, 9]\nदर्शय स") == ["[1, 7, 8, 9, 3]"]

    def test_inserts_with_an_empty_slice(self):
        assert out("स = [1, 2]\nस[1:1] = [5]\nदर्शय स") == ["[1, 5, 2]"]

    def test_deletes_with_an_empty_replacement(self):
        assert out("स = [1, 2, 3, 4]\nस[1:3] = []\nदर्शय स") == ["[1, 4]"]

    def test_negative_and_open_bounds(self):
        assert out("स = [1, 2, 3]\nस[-1:] = [9, 8]\nदर्शय स") == ["[1, 2, 9, 8]"]
        assert out("स = [1, 2, 3]\nस[:1] = [0]\nदर्शय स") == ["[0, 2, 3]"]

    def test_requires_a_list_replacement(self):
        error = error_of("स = [1, 2]\nस[0:1] = 5\n")
        assert "सूची" in error.message

    def test_strings_are_immutable(self):
        error = error_of('श = "ब्रह्म"\nश[0:1] = ["ब"]\n')
        assert "सूची" in error.message or "अपरिवर्तनीय" in error.message

    def test_non_integer_bounds_are_rejected(self):
        error = error_of('स = [1, 2]\nस[0:\"अ\"] = [1]\n')
        assert "पूर्णांक" in error.message

    def test_bytecode_round_trip(self, tmp_path):
        from brahma import compile_source, dump_bytecode, load_bytecode
        from brahma.vm import VM

        path = str(tmp_path / "slice.sbc")
        dump_bytecode(compile_source("स = [1, 2, 3]\nस[1:] = [7]\nदर्शय स\n"), path)
        lines = []
        VM(out=lines.append).run(load_bytecode(path))
        assert lines == ["[1, 7]"]


class TestScopeDeclarations:
    """``बाह्य`` / ``वैश्विक`` — closures can now write through (3.5)."""

    def test_nonlocal_counter_keeps_state(self):
        source = (
            "कार्य काउंटर()\n"
            "    स्थापय गिनती = 0\n"
            "    कार्य बढ़ाओ()\n"
            "        बाह्य गिनती\n"
            "        गिनती = गिनती + 1\n"
            "        प्रत्यागमन गिनती\n"
            "    अन्त\n"
            "    प्रत्यागमन बढ़ाओ\n"
            "अन्त\n"
            "c = काउंटर()\n"
            "दर्शय c()\n"
            "दर्शय c()\n"
            "दर्शय c()\n"
        )
        assert out(source) == ["1", "2", "3"]

    def test_two_counters_are_independent(self):
        source = (
            "कार्य काउंटर()\n"
            "    स्थापय गिनती = 0\n"
            "    कार्य बढ़ाओ()\n"
            "        बाह्य गिनती\n"
            "        गिनती = गिनती + 1\n"
            "        प्रत्यागमन गिनती\n"
            "    अन्त\n"
            "    प्रत्यागमन बढ़ाओ\n"
            "अन्त\n"
            "a = काउंटर()\n"
            "b = काउंटर()\n"
            "a()\n"
            "a()\n"
            "दर्शय a()\n"
            "दर्शय b()\n"
        )
        assert out(source) == ["3", "1"]

    def test_global_declaration_writes_module_scope(self):
        source = (
            "कुल = 0\n"
            "कार्य जोड़ो(n)\n"
            "    वैश्विक कुल\n"
            "    कुल = कुल + n\n"
            "अन्त\n"
            "जोड़ो(5)\n"
            "जोड़ो(7)\n"
            "दर्शय कुल\n"
        )
        assert out(source) == ["12"]

    def test_two_names_in_one_declaration(self):
        source = (
            "कार्य f()\n"
            "    स्थापय a = 1\n"
            "    स्थापय b = 2\n"
            "    कार्य g()\n"
            "        बाह्य a, b\n"
            "        a = a + 10\n"
            "        b = b + 20\n"
            "    अन्त\n"
            "    g()\n"
            "    प्रत्यागमन [a, b]\n"
            "अन्त\n"
            "दर्शय f()\n"
        )
        assert out(source) == ["[11, 22]"]

    def test_read_only_closures_still_work(self):
        source = (
            "कार्य f()\n"
            "    स्थापय x = 5\n"
            "    कार्य g()\n"
            "        प्रत्यागमन x\n"
            "    अन्त\n"
            "    प्रत्यागमन g\n"
            "अन्त\n"
            "g = f()\n"
            "दर्शय g()\n"
        )
        assert out(source) == ["5"]

    def test_declaration_outside_a_function_is_rejected(self):
        error = error_of("बाह्य x\n")
        assert "कार्य" in error.message

    def test_undeclared_outer_name_falls_back_to_globals(self):
        source = (
            "कार्य f()\n"
            "    बाह्य नया\n"
            "    नया = 7\n"
            "अन्त\n"
            "f()\n"
            "दर्शय नया\n"
        )
        assert out(source) == ["7"]

    def test_declarations_survive_a_bytecode_round_trip(self, tmp_path):
        from brahma import compile_source, dump_bytecode, load_bytecode
        from brahma.vm import VM

        source = (
            "कार्य काउंटर()\n"
            "    स्थापय n = 0\n"
            "    कार्य जोड़ो()\n"
            "        बाह्य n\n"
            "        n = n + 1\n"
            "        प्रत्यागमन n\n"
            "    अन्त\n"
            "    प्रत्यागमन जोड़ो\n"
            "अन्त\n"
            "c = काउंटर()\n"
            "c()\n"
            "दर्शय c()\n"
        )
        path = str(tmp_path / "scope.sbc")
        dump_bytecode(compile_source(source), path)
        lines = []
        VM(out=lines.append).run(load_bytecode(path))
        assert lines == ["2"]
