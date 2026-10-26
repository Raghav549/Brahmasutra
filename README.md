# BRAHMA 🕉️

**A Sanskrit-native programming language — with a real compiler, bytecode format and virtual machine.**

[![CI](https://github.com/Raghav549/Brahmasutra/actions/workflows/python-package.yml/badge.svg)](https://github.com/Raghav549/Brahmasutra/actions/workflows/python-package.yml)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-lightgrey)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-326%20passing-brightgreen)](tests/)

```brahma
कार्य फिब(n)
    यदि n < 2
        प्रत्यागमन n
    अन्त
    प्रत्यागमन फिब(n - 1) + फिब(n - 2)
अन्त

स्थापय i = 0
यावत् i <= 10
    दर्शय फिब(i)
    i = i + 1
अन्त
```

```
$ brahma run examples/फिबोनाची.sutra
0
1
1
2
3
5
8
13
21
34
55
89
144
```

BRAHMA is a small, dynamically typed language whose native vocabulary is
Sanskrit. Every keyword also has an ASCII alias, so the same program can be
written with `if` / `while` / `print` if you prefer.

---

## Status: what is real, what is prototype

This repository used to be a collection of ~700 prototype files from many
generations of the project, with no working engine and no tests. It has been
audited end-to-end (**[docs/AUDIT.md](docs/AUDIT.md)**) and the language core has
been rebuilt on a sound footing.

| Component | Status |
|---|---|
| `brahma/` — lexer, parser, compiler, bytecode, VM, CLI | ✅ **stable**, 326 tests, 93 % coverage |
| `examples/` — 7 runnable programs | ✅ works |
| `tests/` — unit, integration, CLI, legacy regression | ✅ works, runs in CI on Python 3.9–3.12 |
| `native_vm/` — a small independent C virtual machine | 🧪 prototype (works, subset of the language) |
| `kernel/`, `os/` — C shell + "ISO" | 🧪 prototype; the `.iso` is not bootable |
| `सूत्र_*.py`, `ब्रह्म_*.py`, `*_तंत्र.py` (≈700 files) | 📦 **legacy**, kept for provenance, pinned by `tests/legacy_baseline.json` |
| `apk/`, `output/*.apk`, generated app trees | 📦 artifacts of an earlier experiment; most are not valid APKs |
| "AI engine" modules | ⚠️ **not AI** — template/keyword-based scaffolding (see audit C-7) |

The audit explains every claim and every defect, with file references and
numbers you can reproduce yourself.

---

## Install

```bash
git clone https://github.com/Raghav549/Brahmasutra
cd Brahmasutra
python -m pip install -e ".[dev]"     # engine + pytest + flake8
```

No runtime dependencies: the engine uses the Python standard library only.
Requires Python 3.9+.

## Quick start

```bash
brahma version
brahma run examples/नमस्ते.sutra
brahma run examples/अभाज्य.sutra
brahma repl
```

The same commands work without installing:

```bash
python -m brahma run examples/नमस्ते.sutra
```

### CLI

| Command | Description |
|---|---|
| `brahma run FILE.sutra` | compile and execute |
| `brahma check FILE.sutra` | parse + compile only (fast CI gate) |
| `brahma compile FILE.sutra -o FILE.sbc` | emit versioned bytecode |
| `brahma disasm FILE.sutra\|FILE.sbc` | readable bytecode listing |
| `brahma run-bytecode FILE.sbc` | execute compiled bytecode |
| `brahma repl` | interactive shell (supports multi-line blocks) |
| `brahma version` | print the version |

Exit codes: `0` success · `1` program or I/O error · `2` usage error.

### Python API

```python
from brahma import run_source, compile_source, VM

result = run_source('दर्शय 2 + 3')
assert result.ok
assert result.output == ["5"]

code = compile_source('दर्शय "नमस्ते"')   # CodeObject
print(code.instructions)                  # [LOAD_CONST, PRINT, HALT]
```

---

## The language in one page

* **Keywords in Devanagari and ASCII** — `यदि`/`if`, `यावत्`/`while`, `कार्य`/`func`,
  `दर्शय`/`print`, `प्रत्यागमन`/`return`, `सत्य`/`true`, `च`/`and`, `वा`/`or`, `न`/`not`.
* **Devanagari numerals** — `१० + ५` is `15`.
* **Blocks end with `अन्त`** (`end`); indentation is cosmetic.
* **Real expressions** — 11 precedence levels, `**` (right-associative), short-circuit logic.
* **Functions and recursion** — parameters, locals, early return, call-depth limit.
* **Lists and strings** — literals, indexing (including negative), element assignment, concatenation.
* **Diagnostics with positions** — `file.sutra:4:5: अपरिभाषित नाम 'अ'` plus a call trace.
* **Two guards against runaway programs** — an instruction budget and a call-depth limit.

Full grammar, semantics, builtins and the bytecode specification:
**[docs/LANGUAGE.md](docs/LANGUAGE.md)**.

---

## Architecture

```
source .sutra
    │
    ▼
 brahma/lexer.py      tokens (Unicode identifiers, ०-९ numerals, strings, comments)
    │
    ▼
 brahma/parser.py     AST (ast_nodes.py) — recursive descent, 11 precedence levels
    │
    ▼
 brahma/compiler.py   CodeObject tree — jump patching, loop contexts, function objects
    │
    ▼
 brahma/bytecode.py   versioned .sbc container (SUTRA1 + JSON), validation, disassembler
    │
    ▼
 brahma/vm.py         stack VM — frames, locals/globals, 12 builtins, limits, tracebacks
```

Everything is pure Python, dependency-free, and deterministic — which is why the
suite runs in ~5 seconds and can pin the behaviour of the legacy tree.

## Repository layout

| Path | What it is |
|---|---|
| `brahma/` | **the engine** (this is the product) |
| `examples/` | runnable Sanskrit programs |
| `tests/` | 326 tests, including the legacy regression matrix |
| `docs/LANGUAGE.md` | language reference + bytecode spec |
| `docs/TESTING.md` | how to run and extend the test suite |
| `docs/AUDIT.md` | **full project audit** — findings, evidence, roadmap |
| `tools/legacy_baseline.py` | records/verifies the legacy demo matrix |
| `native_vm/`, `kernel/`, `os/` | earlier C experiments (prototype) |
| `सूत्र_*.py`, `ब्रह्म_*.py`, `*_तंत्र.py`, `सर्वनिर्माण_v*` | legacy prototype tree |

## Testing

```bash
pytest -q                                  # 326 passed, 12 xfailed in ~5 s
pytest -q --cov=brahma --cov-report=term-missing
flake8 brahma tests tools
python tools/legacy_baseline.py --check    # every legacy demo is accounted for
```

CI runs lint, a syntax sweep of **all** Python files, the suite on Python
3.9–3.12, CLI smoke tests, a wheel build + clean install, the legacy baseline
check, and an optional build of the C VM.

## Roadmap

1. Consolidate the ~700 legacy modules into `legacy/` and keep one implementation per subsystem.
2. Port the OS-style layer (process/memory/scheduler/syscall) onto the new VM as `brahma/os/`.
3. Make the APK/ISO artifacts real — or remove the claim and the binaries.
4. Replace the template "AI" layer with a real model integration behind an explicit interface.
5. Add `mypy --strict` and property-based tests to CI.

Details and effort estimates: [docs/AUDIT.md §8](docs/AUDIT.md#8-आगे-की-योजना-remaining-roadmap).

## Contributing

Run `pytest` and `flake8 brahma tests tools` before opening a pull request; both
must be clean. New behaviour needs a test. If you touch a legacy demo, regenerate
the baseline (`python tools/legacy_baseline.py`) so the change is recorded.

## License

[CC0 1.0 Universal](LICENSE) — public domain dedication.
