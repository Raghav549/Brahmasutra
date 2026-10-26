# परीक्षण मार्गदर्शिका (Testing Guide)

## Quick start

```bash
python -m pip install -e ".[dev]" pytest-cov
pytest -q                                   # 587 tests, ~34 s
pytest -q --cov=brahma --cov-report=term-missing
flake8 brahma tests tools brahma_llm
```

Expected result: **587 passed, 0 xfailed**, 93 % statement coverage of the
engine, `flake8` exit code 0.

## Layout

| Path | Purpose |
|---|---|
| `tests/test_lexer.py` | tokens, Unicode identifiers, Devanagari numerals, escapes, lexical errors |
| `tests/test_parser.py` | AST shape, precedence, block structure, parse diagnostics |
| `tests/test_compiler.py` | emitted opcodes, jump patching, validation |
| `tests/test_bytecode.py` | `.sbc` round-trip, format/version guards, disassembler |
| `tests/test_vm.py` | semantics: arithmetic, strings, lists, logic, control flow, functions, builtins, limits, tracebacks |
| `tests/test_cli.py` | every CLI command (subprocess **and** in-process), REPL |
| `tests/test_integration.py` | all example programs, source↔bytecode equivalence, public API, packaging |
| `tests/test_legacy.py` | the historical demo tree: 51 scripts + 23 module imports, pinned to a baseline |
| `tests/test_web_stack.py` | web stack, chat backend, bytecode format, CLI helper, generators, packaging, AI model |
| `tests/test_llm.py` | ब्रह्म-LLM: tokenizer, n-gram + neural LM, **gradient check**, सूत्र↔Python forward pass, kernel image, generator validity, self-editing invariants, autonomous loop, agent (chat·code·run·explain·image), HTTP server, `brahma llm` CLI |
| `tests/conftest.py` | helpers (`output_of`, `repo_copy` sandbox fixture) |
| `tools/legacy_baseline.py` | regenerates / verifies the legacy baseline |

## The legacy baseline

The repository keeps ~700 prototype files from earlier generations. They are
**not** deleted (provenance) and **not** silently ignored (that is how they rotted
in the first place). Instead:

* `tests/legacy_baseline.json` records, for every top-level demo script, whether
  it exits 0, fails, or hangs, **and the last error line**.
* `tests/test_legacy.py` asserts that anything recorded as working still works.
  Anything recorded as broken is reported as an **xfail** with its original error
  text, so it stays visible in every test run.
* a test fails if a new `*test*.py` script appears without a baseline entry.

When you fix a legacy script:

```bash
python tools/legacy_baseline.py        # runs every demo in a sandbox copy
git diff tests/legacy_baseline.json    # the fix shows up as pass ← fail
```

The tool never writes into the checkout: it copies the repository to a temporary
directory first, because several demos write output files into the working
directory.

## The sub-directory demo sweep

`tools/demo_sweep.py` runs the 264 scripts that live in sub-directories
(`कृत्रिमबुद्धि/`, `engine/`, `vm/`, the demo app backends, …), which the legacy
baseline does not cover. It classifies each script as `ok`, `usage` (needs
arguments or a terminal), `server` (a socket/GUI loop that is *supposed* to
block — the unit suite smoke-tests those with `--once`) or `fail`.

```bash
python tools/demo_sweep.py --check          # exit 1 if anything fails
python tools/demo_sweep.py --json report.json
```

Current measured result: **232 ok, 26 servers, 6 usage, 0 failures** in ~11 s.
Before 2.0.0 the same sweep found **49** failures: scripts that could not import
their own package, demos that raised `EOFError` without a terminal, and two
programs with working-directory-relative paths.

## CI jobs (`.github/workflows/python-package.yml`)

| Job | What it proves |
|---|---|
| `Lint` | `flake8` is clean for `brahma/ tests/ tools/`; every `.py` file in the **whole** repository still compiles |
| `Test` | matrix Python 3.9–3.12: full suite + coverage + CLI smoke (`run`, `compile`, `disasm`, `run-bytecode`) |
| `Legacy baseline freshness` | `python tools/legacy_baseline.py --check` — no demo is missing from the matrix |
| `Package` | sdist + wheel build, install into a clean venv, `brahma version`, run an example |
| `Native` | the optional C VM compiles with `gcc -Wall` and executes a sample (non-blocking) |

## Writing a test

```python
from brahma import execute

def test_something():
    result = execute('दर्शय 2 + 3')
    assert result.ok, result.error.format()
    assert result.output == ["5"]
```

Rules that keep the suite honest:

1. **Assert**, don't just run. A script that prints is not a test.
2. Assert the **reason** of an error, not only that it was raised.
3. Never import a demo module at test-module import time (many print or block on
   `input()`); use the subprocess helpers in `conftest.py`.
4. Never write into the repository from a test; use `tmp_path` or `repo_copy`.
5. Keep the suite under ~10 s so it is run on every edit.

## Coverage policy

`brahma/` is expected to stay above 85 %. `brahma/__main__.py` and a few
defensive branches (`# pragma: no cover`) are excluded by nature. CLI code is
covered both through subprocess tests and in-process `main([...])` calls.
