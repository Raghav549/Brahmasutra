"""End-to-end tests: example programs, the public API and packaging."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

import brahma
from brahma import execute
from brahma.api import (
    build_bytecode_file,
    compile_file,
    compile_source_to_code,
    disassemble,
    load_and_run,
    render,
    run_file,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(REPO_ROOT, "examples")


def example_files():
    return sorted(name for name in os.listdir(EXAMPLES) if name.endswith(".sutra"))


def test_examples_exist():
    assert example_files(), "examples/ में कम से कम एक कार्यक्रम होना चाहिए"


@pytest.mark.parametrize("name", example_files())
def test_example_runs(name):
    result = run_file(os.path.join(EXAMPLES, name))
    assert result.ok, "%s: %s" % (name, result.error.format() if result.error else "")
    assert result.output, "%s produced no output" % name


@pytest.mark.parametrize("name", example_files())
def test_example_bytecode_matches_source(name, tmp_path):
    """Compiled execution must be identical to direct execution."""
    path = os.path.join(EXAMPLES, name)
    direct = run_file(path)
    code = compile_file(path)
    target = str(tmp_path / (name + ".sbc"))
    from brahma.bytecode import dump_bytecode

    dump_bytecode(code, target)
    compiled = load_and_run(target)
    assert compiled.ok, compiled.error.format() if compiled.error else ""
    assert compiled.output == direct.output


class TestExampleOutputs:
    def test_hello(self):
        assert run_file(os.path.join(EXAMPLES, "नमस्ते.sutra")).output == ["नमस्ते, विश्व!"]

    def test_fibonacci(self):
        output = run_file(os.path.join(EXAMPLES, "फिबोनाची.sutra")).output
        assert output[:7] == ["0", "1", "1", "2", "3", "5", "8"]
        assert output[-1] == "144"

    def test_factorial(self):
        output = run_file(os.path.join(EXAMPLES, "क्रमगुणन.sutra")).output
        assert "10! = 3628800" in output

    def test_primes(self):
        output = run_file(os.path.join(EXAMPLES, "अभाज्य.sutra")).output
        assert output[-1] == "कुल अभाज्य: 15"
        assert output[:5] == ["2", "3", "5", "7", "11"]

    def test_fizzbuzz(self):
        output = run_file(os.path.join(EXAMPLES, "फ़िज़बज़.sutra")).output
        assert output[2] == "फ़िज़"
        assert output[4] == "बज़"
        assert output[14] == "फ़िज़बज़"
        assert len(output) == 20

    def test_lists(self):
        output = run_file(os.path.join(EXAMPLES, "श्रेणी.sutra")).output
        assert "कुल योग: 114" in output


class TestPublicApi:
    def test_version(self):
        assert brahma.__version__ == "1.0.0"

    def test_execute_captures_output(self):
        result = execute('दर्शय "x"')
        assert result.ok
        assert result.output == ["x"]
        assert result.steps > 0
        assert result.elapsed >= 0

    def test_execute_forwards_output(self):
        seen = []
        execute("दर्शय 1", out=seen.append)
        assert seen == ["1"]

    def test_execute_reports_errors(self):
        result = execute("दर्शय 1 / 0")
        assert not result.ok
        assert "शून्य" in result.error.message

    def test_compile_source_to_code(self):
        code = compile_source_to_code("दर्शय 1")
        assert code.name == "<module>"

    def test_disassemble(self):
        assert "HALT" in disassemble("दर्शय 1")

    def test_build_bytecode_file(self, tmp_path):
        source = tmp_path / "a.sutra"
        source.write_text("दर्शय 1\n", encoding="utf-8")
        target = str(tmp_path / "a.sbc")
        size = build_bytecode_file(str(source), target)
        assert size == os.path.getsize(target)

    def test_render(self):
        assert render(execute("दर्शय 1")) == "1"

    def test_render_error(self):
        assert "शून्य" in render(execute("दर्शय 1 / 0"))

    def test_run_file_missing(self):
        with pytest.raises(FileNotFoundError):
            run_file("no_such_file.sutra")


class TestPackaging:
    def test_module_entry_point(self):
        completed = subprocess.run(
            [sys.executable, "-m", "brahma", "version"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        assert completed.returncode == 0
        assert b"1.0.0" in completed.stdout

    def test_package_imports_no_side_effects(self):
        completed = subprocess.run(
            [sys.executable, "-c", "import brahma"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        assert completed.returncode == 0
        assert completed.stdout == b"", "import brahma must not print anything"

    def test_all_exports_exist(self):
        for name in brahma.__all__:
            assert hasattr(brahma, name), name

    def test_pyproject_declares_testpaths(self):
        with open(os.path.join(REPO_ROOT, "pyproject.toml"), encoding="utf-8") as handle:
            content = handle.read()
        assert 'testpaths = ["tests"]' in content
