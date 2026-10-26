# BRAHMA 🕉️

**A Sanskrit-native programming language — with a real compiler, bytecode format,
virtual machine, its own OS kernel, and a from-scratch trainable language model
that writes सूत्र and retrains itself.**

[![CI](https://github.com/Raghav549/Brahmasutra/actions/workflows/python-package.yml/badge.svg)](https://github.com/Raghav549/Brahmasutra/actions/workflows/python-package.yml)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-lightgrey)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-456%20passing-brightgreen)](tests/)

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
| `brahma/` — lexer, parser, compiler, bytecode, VM, CLI | ✅ **stable**, 456 tests, 93 % coverage |
| `brahma_llm/` — tokenizer, n-gram + neural LM, trainer, self-editor, kernel image, app builder | ✅ **works**, trained from scratch with no ML dependencies (**[docs/LLM.md](docs/LLM.md)**) |
| `examples/` — 7 runnable programs | ✅ works |
| `tests/` — unit, integration, CLI, web stack, legacy regression | ✅ works, runs in CI on Python 3.9–3.12 |
| `brahma_web` / `brahma_chat` — stdlib HTTP + demo backends | ✅ works (no Flask needed) |
| `brahma_bytecode` — one documented bytecode format | ✅ works (assembler, disassembler, machine, boot images) |
| `brahma_ai` — n-gram model + prompt router | ✅ works, honestly labelled (see below) |
| `brahma_packaging` — Android bundles | ✅ builds ZIP bundles; **not** installable APKs |
| `native_vm/` — a small independent C virtual machine | 🧪 prototype (works, subset of the language) |
| `kernel/` — सूत्र-OS shell over the real `SUTRAOS` image | ✅ boots and verifies (`brahma llm kernel verify`) |
| `.iso` images left by the old build scripts | 🧪 prototype; never bootable, kept out of git |
| `सूत्र_*.py`, `ब्रह्म_*.py`, `*_तंत्र.py` (≈700 files) | 📦 **legacy**, but now import-safe: 51/51 demos pass, pinned by `tests/legacy_baseline.json` |

### ब्रह्म-LLM in one screen

```bash
brahma llm train --size small          # train on the repository's सूत्र corpus
brahma llm generate "दर्शय" --tokens 40 # sample text (or `--engine sutra` for the सूत्र VM)
brahma llm complete "कार्य"            # only syntactically valid सूत्र programs are kept
brahma llm autotrain --target "अभाज्य संख्या जाँच लिखो" --iterations 4
brahma llm evolve --body --os          # grow the model, rebuild + verify the kernel
brahma llm kernel verify               # boot SUTRAOS: banner → self-test → READY
brahma llm build-app --target "योग अनुप्रयोग"
brahma llm sutra-math                  # the model's maths, executed by सूत्र itself
```

A measured autonomous run (4 rounds, 9.2 s, `docs/LLM.md` §3.2): 24/24 generated
programs ran, held-out perplexity **10.43 → 8.96 (−14 %)**, hidden layer grown
32 → 48 with **zero** prediction drift, kernel rebuilt and verified.

### Honesty rules this repository follows

* **"APK" means ZIP bundle.** `brahma_packaging.is_installable_apk()` returns
  `False` for everything these builders produce: an installable APK needs a
  compiled manifest, a real DEX and a signature (`aapt2`, `d8`, keystore).
  Builders now say "ZIP संग्रह" instead of claiming an installable app.
* **"AI" means a model or a documented rule.** `brahma_ai.MarkovModel` is a
  real, trainable n-gram model; `brahma_ai.PromptRouter` is a keyword router and
  always reports the rule it matched (`--explain`). `brahma_llm` is a real
  language model — tokenizer, two models, hand-written backpropagation, Adam,
  an autonomous trainer and self-editing — and it is **small**: 4–52 k
  parameters on a ~33 k-character corpus. `brahma llm bench` prints the measured
  perplexities, and `docs/LLM.md` states plainly that this is not a frontier
  model and makes no "largest in the world" claim.
* **No hidden side effects.** Importing any module does nothing; demo code lives
  behind `_main()` and runs through `brahma_cli.चलाओ`, which turns "needs a
  terminal" into exit code 2 instead of a traceback.

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
pytest -q                                  # 456 passed in ~19 s
pytest -q --cov=brahma --cov-report=term-missing
flake8 brahma tests tools                  # 0 issues
python tools/legacy_baseline.py --check    # 51/51 demos pass, none unregistered
python tools/harden_imports.py             # import-time side-effect report
```

CI runs lint, a syntax sweep of **all** Python files, the suite on Python
3.9–3.12, CLI smoke tests, a wheel build + clean install, the legacy baseline
check, and an optional build of the C VM.

## Roadmap

1. Consolidate the ~700 legacy modules into `legacy/` and keep one implementation per subsystem.
2. Port the OS-style layer (process/memory/scheduler/syscall) onto the new VM as `brahma/os/`.
3. Make the APK builder produce a genuinely signed APK (needs `aapt2`/`d8`) — until
   then it builds labelled ZIP bundles.
4. Grow `brahma_ai` beyond n-grams (embedding-based router) behind the same interface.
5. Add `mypy --strict` and property-based tests to CI.

Details and effort estimates: [docs/AUDIT.md §8](docs/AUDIT.md#8-आगे-की-योजना-remaining-roadmap).

## Contributing

Run `pytest` and `flake8 brahma tests tools` before opening a pull request; both
must be clean. New behaviour needs a test. If you touch a legacy demo, regenerate
the baseline (`python tools/legacy_baseline.py`) so the change is recorded.

## License

[CC0 1.0 Universal](LICENSE) — public domain dedication.
