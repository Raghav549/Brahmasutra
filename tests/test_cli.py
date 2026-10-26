"""Command line interface tests (run through a real subprocess)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

from brahma.bytecode import MAGIC

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cli(*args, stdin=None):
    completed = subprocess.run(
        [sys.executable, "-m", "brahma"] + list(args),
        cwd=REPO_ROOT,
        input=None if stdin is None else stdin.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    return completed.returncode, completed.stdout.decode("utf-8"), completed.stderr.decode("utf-8")


def write(tmp_path, name, source):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return str(path)


class TestBasics:
    def test_version_flag(self):
        code, out, _ = cli("--version")
        assert code == 0
        assert "BRAHMA" in out

    def test_version_command(self):
        code, out, _ = cli("version")
        assert code == 0
        assert out.startswith("BRAHMA ")

    def test_no_arguments_prints_help(self):
        code, out, _ = cli()
        assert code == 2
        assert "usage" in out.lower() or "उपयोग" in out.lower()

    def test_unknown_command_fails(self):
        code, _, err = cli("bogus")
        assert code == 2


class TestRun:
    def test_run_prints(self, tmp_path):
        path = write(tmp_path, "hello.sutra", 'दर्शय "नमस्ते"\n')
        code, out, err = cli("run", path)
        assert code == 0, err
        assert out.strip() == "नमस्ते"

    def test_run_quiet(self, tmp_path):
        path = write(tmp_path, "hello.sutra", 'दर्शय "नमस्ते"\n')
        code, out, _ = cli("run", "--quiet", path)
        assert code == 0
        assert out.strip() == ""

    def test_run_arithmetic(self, tmp_path):
        path = write(tmp_path, "a.sutra", "दर्शय 2 + 3 * 4\n")
        code, out, _ = cli("run", path)
        assert code == 0
        assert out.strip() == "14"

    def test_syntax_error_exit_code(self, tmp_path):
        path = write(tmp_path, "bad.sutra", "यदि सत्य\n दर्शय 1\n")
        code, _, err = cli("run", path)
        assert code == 1
        assert "त्रुटि" in err

    def test_runtime_error_shows_line(self, tmp_path):
        path = write(tmp_path, "boom.sutra", "दर्शय 1\nदर्शय 1 / 0\n")
        code, _, err = cli("run", path)
        assert code == 1
        assert ":2" in err

    def test_missing_file(self):
        code, _, err = cli("run", "does_not_exist.sutra")
        assert code == 1
        assert "नहीं मिली" in err

    def test_step_limit_option(self, tmp_path):
        path = write(tmp_path, "loop.sutra", "यावत् सत्य\n i = 1\nअन्त\n")
        code, _, err = cli("run", "--limit", "10", path)
        assert code == 1
        assert "चरण सीमा" in err


class TestCompile:
    def test_compile_creates_bytecode(self, tmp_path):
        source = write(tmp_path, "prog.sutra", "दर्शय 1\n")
        target = str(tmp_path / "prog.sbc")
        code, out, err = cli("compile", source, "-o", target)
        assert code == 0, err
        assert os.path.exists(target)
        with open(target, "rb") as handle:
            blob = handle.read()
        assert blob.startswith(MAGIC)
        payload = json.loads(blob[len(MAGIC) :].decode("utf-8"))
        assert payload["format"] == "brahma-bytecode"

    def test_compile_default_output_name(self, tmp_path):
        source = write(tmp_path, "auto.sutra", "दर्शय 1\n")
        code, _, _ = cli("compile", source)
        assert code == 0
        assert os.path.exists(str(tmp_path / "auto.sbc"))

    def test_compile_error_exit_code(self, tmp_path):
        source = write(tmp_path, "bad.sutra", "दर्शय\n")
        code, _, err = cli("compile", source)
        assert code == 1
        assert "त्रुटि" in err

    def test_run_bytecode(self, tmp_path):
        source = write(tmp_path, "prog.sutra", 'दर्शय "नमस्ते"\n')
        target = str(tmp_path / "prog.sbc")
        assert cli("compile", source, "-o", target)[0] == 0
        code, out, err = cli("run-bytecode", target)
        assert code == 0, err
        assert out.strip() == "नमस्ते"

    def test_run_bytecode_bad_file(self, tmp_path):
        path = tmp_path / "bad.sbc"
        path.write_text("garbage", encoding="utf-8")
        code, _, err = cli("run-bytecode", str(path))
        assert code == 1
        assert "त्रुटि" in err

    def test_disasm_source(self, tmp_path):
        source = write(tmp_path, "prog.sutra", "दर्शय 1\n")
        code, out, _ = cli("disasm", source)
        assert code == 0
        assert "LOAD_CONST" in out
        assert "HALT" in out

    def test_disasm_bytecode(self, tmp_path):
        source = write(tmp_path, "prog.sutra", "दर्शय 1\n")
        target = str(tmp_path / "prog.sbc")
        cli("compile", source, "-o", target)
        code, out, _ = cli("disasm", target)
        assert code == 0
        assert "LOAD_CONST" in out


class TestCheck:
    def test_check_ok(self, tmp_path):
        source = write(tmp_path, "ok.sutra", "दर्शय 1\n")
        code, out, _ = cli("check", source)
        assert code == 0
        assert "ठीक" in out

    def test_check_failure(self, tmp_path):
        source = write(tmp_path, "bad.sutra", "यदि\n")
        code, _, err = cli("check", source)
        assert code == 1
        assert "त्रुटि" in err


class TestRepl:
    def test_expression_is_echoed(self):
        code, out, _ = cli("repl", stdin="1 + 2\n:quit\n")
        assert code == 0
        assert "3" in out

    def test_variables_persist(self):
        code, out, _ = cli("repl", stdin="अ = 10\nअ + 5\n:quit\n")
        assert code == 0
        assert "15" in out

    def test_error_does_not_exit(self):
        code, out, err = cli("repl", stdin="1 / 0\n2 + 2\n:quit\n")
        assert code == 0
        assert "त्रुटि" in (out + err)
        assert "4" in out

    def test_multiline_block(self):
        code, out, _ = cli("repl", stdin="यदि सत्य\nदर्शय 7\nअन्त\n:quit\n")
        assert code == 0
        assert "7" in out

    def test_eof_exits_cleanly(self):
        code, out, _ = cli("repl", stdin="")
        assert code == 0

    def test_print_statement(self):
        code, out, _ = cli("repl", stdin='दर्शय "x"\n:quit\n')
        assert code == 0
        assert "x" in out


class TestInProcess:
    """Call the CLI in-process (fast, and keeps coverage meaningful)."""

    def test_main_version(self, capsys):
        from brahma.cli import main

        assert main(["version"]) == 0
        assert "BRAHMA" in capsys.readouterr().out

    def test_main_no_command(self, capsys):
        from brahma.cli import main

        assert main([]) == 2

    def test_main_run(self, tmp_path, capsys):
        from brahma.cli import main

        path = write(tmp_path, "a.sutra", "दर्शय 5\n")
        assert main(["run", path]) == 0
        assert capsys.readouterr().out.strip() == "5"

    def test_main_run_quiet(self, tmp_path, capsys):
        from brahma.cli import main

        path = write(tmp_path, "a.sutra", "दर्शय 5\n")
        assert main(["run", "--quiet", path]) == 0
        assert capsys.readouterr().out.strip() == ""

    def test_main_check(self, tmp_path, capsys):
        from brahma.cli import main

        path = write(tmp_path, "a.sutra", "दर्शय 5\n")
        assert main(["check", path]) == 0
        assert "ठीक" in capsys.readouterr().out

    def test_main_run_by_bytecode(self, tmp_path, capsys):
        from brahma.cli import main

        source = write(tmp_path, "a.sutra", "दर्शय 5\n")
        target = str(tmp_path / "a.sbc")
        assert main(["compile", source, "-o", target]) == 0
        assert main(["run-bytecode", target]) == 0
        assert capsys.readouterr().out.strip().endswith("5")

    def test_repl_class_evaluates_and_keeps_state(self, capsys):
        from brahma.cli import Repl

        repl = Repl()
        assert repl.handle("अ = 1") is True
        assert repl.handle("अ + 1") is True
        assert "2" in capsys.readouterr().out

    def test_repl_class_quit(self):
        from brahma.cli import Repl

        repl = Repl(out=lambda text: None)
        assert repl.handle(":quit") is False
        assert repl.handle("exit") is False
        assert repl.handle("निर्गम") is False

    def test_repl_class_parse_error_recovers(self, capsys):
        from brahma.cli import Repl

        repl = Repl(out=lambda text: None)
        assert repl.handle("यदि") is True  # keeps waiting for a block
        assert repl.buffer == ["यदि"]
        assert repl.handle("अन्त") is True
        assert repl.buffer == []

    def test_repl_class_runtime_error_recovers(self, capsys):
        from brahma.cli import Repl

        repl = Repl(out=lambda text: None)
        assert repl.handle("1 / 0") is True
        assert repl.buffer == []

    def test_repl_blank_line_is_ignored(self):
        from brahma.cli import Repl

        repl = Repl(out=lambda text: None)
        assert repl.handle("   ") is True
        assert repl.buffer == []


class TestModules:
    """``brahma modules`` — the सूत्र standard library (3.6)."""

    def test_lists_stdlib_modules(self):
        code, stdout, _ = cli("modules")
        assert code == 0
        assert "गणित.सूत्र" in stdout
        assert "पाठ.सूत्र" in stdout

    def test_shows_module_exports(self):
        code, stdout, _ = cli("modules", "गणित")
        assert code == 0
        assert stdout.startswith("गणित — ")
        assert "अभाज्य" in stdout

    def test_unknown_module_fails(self):
        code, _, stderr = cli("modules", "नहीं_है")
        assert code == 1
        assert "मॉड्यूल नहीं मिला" in stderr

    def test_run_program_that_imports_stdlib(self, tmp_path):
        path = tmp_path / "मुख्य.सूत्र"
        path.write_text('आयात "गणित"\nदर्शय वर्ग(9)\n', encoding="utf-8")
        code, stdout, _ = cli("run", str(path))
        assert code == 0
        assert stdout.strip() == "81"
