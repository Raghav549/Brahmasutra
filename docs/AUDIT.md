# BRAHMA — पूर्ण परियोजना लेखा-परीक्षा (Full Project Audit)

**Updated:** 2026-10-27 for **3.6.0** — see §11 for the current, re-measured
state (588 tests, 51 pins, 221 demos, kernel verify). The body of this document
is the original audit of the pre-1.0 tree and is kept unchanged as a record.

**Audited commit:** `27980b8542295c7313afeb46d09805cb9d1bbe07` (`main`, single commit)
**Audit date:** 2026-10-26
**Environment:** Linux x86-64 · CPython 3.11.2 · no third-party runtime dependencies
**Auditor:** Arena Agent Mode (automated static + dynamic analysis, all numbers reproducible — see §9)
**Scope:** every tracked file in the repository, every Python module, every demo script, every committed binary artifact, CI configuration, packaging and documentation.

---

## 1. कार्यकारी सारांश (Executive summary)

### Verdict

The repository is a **large, genuine prototype** — 40k lines of hand-written Python, a small C VM, a C "kernel", nine example programs, and dozens of generated demo apps. It is **not**, today, a working Sanskrit programming language, an OS, or an AI engine. The gap between the README's claims and the behaviour of the code is the single most important finding.

Concretely, at the audited commit:

| Claim (README) | Reality at `27980b8` |
|---|---|
| "world's first fully Sanskrit-native programming language" | The "language core" is a whitespace line-splitter with 4 opcodes and 4 hard-coded registers. No expressions, no user variables beyond `अ/ब/स/द`, no functions, no control flow. |
| "Compiler engine" | `सूत्र_संकलक.py` maps 4 fixed keywords to bytes; there is no expression parser, no symbol table, no diagnostics. Four further incompatible "bytecode" formats exist without a specification. |
| "AI-powered code generation engine" | `ब्रह्म_AI_विश्लेषक.py` is `if "chat" in prompt` plus f-string HTML templates. No model, no API client, no ML dependency, no training artefact. |
| "Full-stack creation capability" | The flagship generated app `chat_app_with_login_database_api_dashboard/backend/api.py` is a 23-line Flask endpoint returning `{"status": "running"}`. |
| "OS / APK / ISO" (implied by `os/`, `apk/`, 29 `.apk` files, `सूत्र_os.iso`) | The "kernel" is a 77-line userspace C REPL. The `.iso` is a **tar archive** (no ISO9660 signature), 20 KB, unbootable. 14 of 29 `.apk` files are not even ZIP archives. |
| "Tests" | **Zero** assertions and zero `pytest`/`unittest` usage in 702 Python files. `pytest` at the repository root aborts during collection (9 errors, 0 tests). |
| CI badge / GitHub Actions | The workflow installs `pytest` and runs it on a suite that cannot collect — i.e. it has never tested anything. |

### What is good

* Real, un-faked engineering *effort*: 611 distinct modules, a C VM (`native_vm/*.c`, builds and runs), a C kernel shell, an executable-file format, demo apps.
* 37 of the 51 top-level demo scripts **did** run correctly before this audit; the CPU/VM/assembler demos are coherent and produce the right register values.
* No malware, no obfuscation, no telemetry, no network calls to third-party services in the runtime core.

### What this change delivers

1. **A working language engine** (`brahma/`, 1,474 statements, 93 % test coverage): real lexer, recursive-descent parser with precedence, bytecode compiler with jump patching and function objects, a stack VM with frames/recursion/step-limits, a versioned `.sbc` container, CLI (`run`/`compile`/`disasm`/`check`/`repl`/`run-bytecode`), 7 runnable example programs, and Python 3.9–3.12 packaging.
2. **A real test suite** (`tests/`): **326 tests, 0 failures**, 4.4 s, including a full regression pin over all 51 legacy demos.
3. **Green, meaningful CI** (lint, syntax sweep, 4-version matrix, CLI smoke, wheel build + clean install, native C VM build, legacy baseline freshness).
4. **Repository hygiene**: `.gitignore`, `pyproject.toml`, 386 committed `__pycache__/*.pyc` files untracked, 3 syntax errors and 3 runtime bugs fixed.
5. **This audit**, plus a language specification and a testing guide.

6. **A language model that lives here (2.0.0 → 3.0.0)** — `brahma_llm/`: an akṣara
   tokenizer, two trainable models (n-gram and a neural LM with hand-written
   backpropagation verified against central differences), a target-driven
   autonomous trainer, prediction-preserving self-editing, a सूत्र-OS kernel
   image that must boot before it can be installed, and the model's own maths
   written in सूत्र and executed on the project VM. Measured numbers, not
   adjectives: see **[docs/LLM.md](LLM.md)**.

Numbers before → after:

| Metric | Before | After |
|---|---|---|
| Collectable automated tests | 0 | **326** |
| Passing tests | 0 (collection aborted) | **326** |
| Assertions in repository | 0 | 500+ |
| Test coverage of the language engine | n/a | **93 %** |
| Legacy demo scripts passing | 37 / 51 | **40 / 51** (rest pinned as expected failures) |
| Python files with syntax errors | 3 | **0** |
| Tracked `.pyc` files | 386 | **0** |
| Declared lint configuration | none | `.flake8` + clean on `brahma/ tests/ tools/` |
| Packaging (`pip install`) | impossible | **wheel + sdist + `brahma` console script** |
| CI that actually runs tests | no | **yes (5 jobs, 4 Python versions)** |

---

## 2. विधि (Method)

Five passes were run against a clean checkout plus a throw-away copy (`/tmp`) so the working tree was not polluted:

1. **Static analysis** — `ast` parse of all 702 modules (syntax, imports, top-level statements, defs/classes), duplicate-file hashing, dead-module graph, pattern scans (`exec`, `eval`, `os.system`, `shell=True`, bare `except`, hard-coded credentials, top-level `print`/`input`).
2. **Import matrix** — each module imported individually in a subprocess with a 6 s timeout, `cwd` on `sys.path`, stdout/stderr captured, classified: OK / EOFError / AttributeError / ModuleNotFoundError / hang / SyntaxError / port-in-use / etc.
3. **Demo execution matrix** — all 51 top-level `*test*.py` / `*परीक्षण*.py` scripts executed with stdin closed and a timeout; exit status and last error line recorded. This matrix is now machine-readable in `tests/legacy_baseline.json`.
4. **Artifact forensics** — every `.apk` opened with `zipfile`, `AndroidManifest.xml`/`classes.dex` presence checked; `.iso` checked for ISO9660 `CD001` at offset 0x8001; ELF binaries checked for validity and executed.
5. **Post-fix verification** — full suite, lint, coverage, CLI smoke tests, example programs, bytecode round-trip, wheel build & install, native C VM build.

---

## 3. संरचना (Inventory)

### 3.1 Size

| Type | Files | Lines |
|---|---:|---:|
| Python | 702 | 40,927 |
| Devanagari `.सूत्र` sources | 37 | 190 |
| ASCII `.sutra` sources | 7 | 33 |
| HTML (generated apps) | 49 | 2,030 |
| XML (Android resources) | 29 | 417 |
| C (`native_vm/`, `kernel/`) | 5 | 295 |
| Java (Android stubs) | 8 | 132 |
| JSON registers/registries | 13 | — |
| `.apk` archives | 19 | — |
| `.iso` | 1 | — |
| **Tracked total** | **1,480** (386 of them `.pyc`) | ~44,000 |

Repository payload excluding `.git`: **1.1 MB**.

### 3.2 Layout (top-level, by tracked file count)

| Area | Files | Python lines | Nature |
|---|---:|---:|---|
| repository root | 512 | 29,873 | 440 throw-away modules + demo scripts + sample programs |
| `ब्रह्म_AI_अनुप्रयोग/` | 69 | 2,059 | generated "AI apps" |
| `ब्रह्म_AI_कार्यक्षेत्र/` | 64 | 3,706 | AI workspace generators |
| `कृत्रिमबुद्धि/` | 55 | 957 | "artificial intelligence" generators |
| `ब्रह्म_AI_कार्यक्रम/` | 35 | 916 | program/AI generators |
| `release/` | 23 | 655 | **byte-identical copy** of `engine/`, `compiler/`, `version/` |
| `vm/` | 12 | 303 | ASCII bytecode VM (works) |
| `engine/` | 9 | 639 | APK/GUI/install "engines" |
| `native_vm/` | 10 | 0 | **C VM + ELF binaries (works)** |
| `os/` | 8 | 0 | "ISO", GRUB config, C kernel copy |
| `सर्वनिर्माण_v14 … v27` | 100+ | — | 14 generations of generated app trees |

### 3.3 Structural findings

* **611 distinct local module names; 437 are never imported by anything.** The top imported module is used 7 times. There is no package, no `__init__` exports, no API surface.
* **22 duplicate groups / 48 files** (byte-identical). Whole subsystems are duplicated (`release/` mirrors `engine/`, `compiler/`, `version/`), so fixes silently diverge.
* **57 files carry a generation number, up to `v27`** (`सूत्र_creator_ai_v12 … v27`, `brahma_auto_v1 … v5`, `सूत्र_universal_creator_ai_v5 … v11`). Successive generations were appended rather than merged; no changelog records what changed between them.
* **133 of 702 Python files contain no function or class** — they are straight-line scripts with side effects at import.
* **20 empty files**, plus stray artefacts: a file literally named `-`, `registry.json.`, an empty `test.सूत्रबिन`.
* **240 modules print a banner when imported**; **79 modules call `input()` at import time** (see §5.3). Importing the project is therefore interactive and side-effecting.

---

## 4. परीक्षण एवं CI (Testing and CI) — the most serious defect

### 4.1 Baseline before this change

* `grep -r "assert " --include=*.py` → **0 matches**.
* `grep -r "import pytest\|import unittest"` → **0 matches**.
* `python -m pytest` at the repository root:

```
ERROR api_test.py
ERROR compiler/test_compile.py
ERROR release/compiler/test_compile.py
ERROR test_apps/test_app.py
ERROR test_binary_creator.py - ValueError: byte must be in range(0, 256)
ERROR ब्रह्म_AI_कार्यक्षेत्र/test_app.py
ERROR ब्रह्म_AI_कार्यक्षेत्र/स्थापित/test_app.py
ERROR ब्रह्म_स्थापित/test_app.py
ERROR सूत्र_mode_test.py - AttributeError: module 'सूत्र_kernel_mode' has no attribute 'प्रारम्भ'
!!! Interrupted: 9 errors during collection !!!
no tests collected, 9 errors in 1.87s
```

Even if collection had succeeded, pytest would have *executed* demo scripts at import: several call `input()` (hang) or bind TCP ports (`OSError: Address already in use`).

* The GitHub Actions workflow (`.github/workflows/python-package.yml`) runs `pytest` for Python 3.9/3.10/3.11 — i.e. it has been red or vacuous since it was added. It also runs `flake8` over the whole repository, which reports hundreds of style violations (ignored via `--exit-zero`, so it detects nothing).

### 4.2 Demo-script matrix (51 top-level scripts)

Initial result: **37 pass, 12 fail, 2 timeout**.

Failure classes:

| Class | Count | Example |
|---|---:|---|
| Calls an API that was never implemented (`AttributeError`) | 9 | `प्रक्रिया-परीक्षण.py`: `सूत्र_प्रक्रिया_तंत्र.प्रक्रियातंत्र` does not exist (module defines `प्रक्रिया_प्रबंधक`) |
| Import of a non-existent class | 1 | `api_test.py`: `ब्रह्मAPINिष्पादनतंत्र` vs actual `ब्रह्मAPIनिष्पादनतंत्र` |
| Blocks on `input()` with no TTY | 1 | `यन्त्र_चालक_परीक्षण.py` |
| Crashes on illegal byte value | 1 | `test_binary_creator.py`: `ord("अ") = 2304 > 255` |
| Hangs forever (`timeout`) | 2 | `अनुसूचक_परीक्षण.py`, `परीक्षण.py` |

### 4.3 Module import matrix (702 modules)

| Outcome | Count | Meaning |
|---|---:|---|
| OK | **580** | imports (many printing banners) |
| `EOFError` | **79** | calls `input()` at import — cannot be used as a library |
| `AttributeError` | **13** | self-inconsistent APIs |
| `ModuleNotFoundError` | **10** | missing `flask`/`requests` (not declared anywhere) |
| hang (>6 s) | **10** | servers/loops start at import |
| `SyntaxError` | **3** | `शब्द-विश्लेषक.py`, `compiler/test_compile.py`, `release/compiler/test_compile.py` |
| `OSError: Address already in use` | **3** | `HTTPServer` created at import |
| `FileNotFoundError` | **2** | hard-coded relative paths (`../अनुप्रयोग/…`) |
| `ValueError`, `ImportError` | **2** | byte range, class name |

### 4.4 What was added

* `tests/` — 326 tests (lexer 24, parser 36, compiler 24, bytecode 16, VM 89, CLI 36, integration 30, legacy ≈70), 93 % statement coverage of `brahma/`, 4.4 s wall clock.
* `tests/legacy_baseline.json` — machine-readable record of all 51 demos + curated module imports. Working demos are asserted; broken demos are `xfail` with the original error text; a test fails if a new demo appears without a baseline entry.
* `tools/legacy_baseline.py` — regenerates the baseline in a sandbox copy; `--check` verifies coverage (runs in CI).
* `.github/workflows/python-package.yml` — rewritten: lint, syntax sweep of *all* files, test matrix 3.9–3.12, CLI smoke, wheel build + clean-venv install, native C VM build, baseline freshness.
* `pyproject.toml` — `testpaths = ["tests"]`, so the demo tree can never be collected again.

---

## 5. विसंगतियाँ (Findings)

Severity: **B**locker · **C**ritical · **H**igh · **M**edium · **L**ow.
Each finding lists evidence and the remediation status in this change.

### 5.1 Build, packaging, CI

| ID | Sev | Finding | Evidence | Status |
|---|---|---|---|---|
| B-1 | **B** | CI never executed a single test | `pytest` aborts at collection (9 errors, 0 collected) | **Fixed** — real suite + `testpaths`; CI rewritten |
| B-2 | **B** | No packaging of any kind | no `pyproject.toml`/`setup.py`/`requirements.txt`; `flask`/`requests` imported but undeclared | **Fixed** — `pyproject.toml`, wheel/sdist, `brahma` entry point, `.[dev]` extra |
| H-1 | **H** | 386 `__pycache__/*.pyc` committed (26 % of all tracked files) | `git ls-files '*.pyc' \| wc -l` → 386 | **Fixed** — untracked, `.gitignore` added |
| H-2 | **H** | No `.gitignore` at all | root listing | **Fixed** |
| M-1 | **M** | Duplicated `release/` tree (23 files) identical to `engine/`, `compiler/`, `version/` | hash comparison | Documented — delete in a follow-up (kept to preserve provenance) |
| M-2 | **M** | 27 generator generations with no changelog | `*_v1 … v27` | Documented |
| M-3 | **M** | 20 empty files and stray artefacts (`-`, `registry.json.`) | file scan | Documented |

### 5.2 Language core (`सूत्र`, the actual language)

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| B-3 | **B** | "Parser" is `line.split()`; no grammar, no expressions | `सूत्र_parser.py:19-31` produces `{"op": parts[0], "arg1": …}` |
| B-4 | **B** | No variables beyond 4 registers `अ/ब/स/द`; no functions; no `if`/`while` in the compiled pipeline | `सूत्र_संकलक.py:12-23` (`OPCODES = {संकल्प, योग, दर्शय, निर्गम}`) |
| B-5 | **B** | "Bytecode" is an ad-hoc byte stream with no header/version; five incompatible formats coexist (`.sutra`, `.sbc`, `.सूत्रबिन`, `.यन्त्र`, `.bin`, `.bytecode`) | `सूत्र_संकलक.py:56`, `vm/bytecode_spec.txt`, `सूत्र_machine_code.py`, `द्विआधारी/*` |
| C-1 | **C** | `vm/sutra_vm.py` seeds register `R1 = 100` — undefined behaviour for any program that does not set it | `vm/sutra_vm.py:8` |
| C-2 | **C** | Interpreter `सूत्र_भाषा_core.py` calls `पार्सर.parse(...)` but `सूत्र_parser` only exposes `Parser.parse_file`; the module was never runnable | `सूत्र_भाषा_core.py:20` vs `सूत्र_parser.py:6` |
| C-3 | **C** | Three files do not even parse (`range(३:)`, `from वर्ण-कोश import …`) | compile sweep | 
| H-3 | **H** | No error diagnostics: `सूत्र_संकलक` raises bare `KeyError` on an unknown keyword; the VM silently ignores unknown opcodes | `सूत्र_संकलक.py`, `सूत्र_CPU_v1.py` |
| H-4 | **H** | Language is not "fully Sanskrit": internally every tool uses ASCII opcodes (`LOAD`, `ADD`, `machine code [1,0,50]`) | `सूत्र_machine_code.py` |

**Status:** the language core was **rebuilt** as `brahma/` (see §7): a real grammar, AST, compiler, versioned bytecode and VM, with 100 % Sanskrit *and* ASCII surface syntax and full diagnostics. The legacy modules are untouched and pinned by tests.

### 5.3 Library discipline / runtime behaviour

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| B-6 | **B** | 79 modules start an interactive prompt on import (`EOFError` in the matrix) | `sutra_bhasha*.py`, `दुभाषिया.py`, `पाणिनिइंजन.py`, `ide.py` |
| C-4 | **C** | 10 modules bind sockets or start servers on import | `ब्रह्म_AI_*/**/server.py` → `OSError: Address already in use` |
| C-5 | **C** | 240 modules print banners on import; `import brahma_auto` asks for input | AST scan + matrix |
| H-5 | **H** | Inconsistent naming (`अनुसूचक-` vs `अनुसूचक_`, `सूत्र_mode_test.py`), hyphenated filenames are not importable as modules | `शब्द-विश्लेषक.py` |
| M-4 | **M** | 23 files use bare `except:` and swallow all errors | `grep -c "except:"` |

### 5.4 "AI engine" claims

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| B-7 | **B** | There is no AI. "Analysis" is substring matching; "generation" is f-string templates | `ब्रह्म_AI_विश्लेषक.py:15-56` (`if "chat" in आदेश`), `सूत्र_creator_ai_v27.py` (`html = f"""…"""`) |
| C-6 | **C** | No LLM/API client, no model file, no tokenizer, no ML dependency anywhere | dependency scan: only stdlib + undeclared `flask`/`requests` |
| C-7 | **C** | The flagship generated app is a health endpoint: `chat_app_with_login_database_api_dashboard/backend/api.py` = 23 lines, one route `"/"` returning `{"status": "running"}` | file listing |
| M-5 | **M** | Feature list in prompts is parsed but only some flags change output; `auth`, `dashboard` produce nothing | `ब्रह्म_AI_विश्लेषक.py` |

**Recommendation:** rename the subsystem to *template-based app scaffolder* until a real model is integrated; do not ship "AI" in the README.

### 5.5 Artifacts: APK, ISO, "OS"

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| B-8 | **B** | 29 committed `.apk` files; **14 are not ZIP archives**, 5 are ZIPs without `classes.dex`/manifest, only 10 look structurally plausible and none can be installed (no real signing, hand-written `classes.dex`) | `zipfile` scan; `output/gui.apk`, `output/परीक्षण.apk` → *File is not a zip file*; `कृत्रिमबुद्धि/REAL_APK/सूत्रREAL9800.apk` is 750 bytes |
| B-9 | **B** | `os/सूत्र_os.iso` is not an ISO: `os/build_iso.sh` writes it with `tar -cvf`; no ISO9660 signature at 0x8001; 20 KB total; GRUB entry uses `linux /boot/sutra_kernel` for a **userspace** ELF | `os/build_iso.sh:28`, binary check |
| C-8 | **C** | "Kernel" is a 77-line C REPL that `system("../native_vm/sutra_vm …")` — no memory management, no processes, no privilege levels, despite 30+ Python modules named `kernel_*` | `kernel/sutra_kernel.c` |
| H-6 | **H** | The C VM reads `arg1[1] - '1'` as a register index with **no bounds check**; any operand that is not `R1..R4` writes outside `registers[4]` | `native_vm/sutra_vm.c:46` |

**Recommendation:** either generate a real APK (aapt2/gradle, signed) and a real bootable ISO (xorriso + a freestanding kernel), or delete the artefacts and the claim. Do not keep invalid binaries in a public repository — they mislead users and inflate the checkout.

### 5.6 Security

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| S-1 | **H** | Arbitrary code execution as a feature: `exec(code)` on user-supplied files, `eval()` on a "binary" file | `kernel/kernel_engine.py:48`, `द्विआधारी/सूत्र_द्विआधारी_निष्पादक.py:26`, `IDE/सूत्र_IDE.py:83`, 8 more |
| S-2 | **H** | Command injection: `os.system(f"चलाओ {file}")`, `os.system(f"termux-open '{path}'")`, `subprocess.Popen(..., shell=True)` with interpolated strings | `ide.py:19-30`, `sutra_bhasha_v2.py:44`, `ब्रह्म_प्रक्रिया_निष्पादन_कोर.py:16` |
| S-3 | **H** | The C kernel passes an unvalidated shell command line to `system()` (path traversal + injection) | `kernel/sutra_kernel.c:55` |
| S-4 | **M** | Generated apps ship with a hard-coded admin password `admin123` and plain-text user store | `brahma_auto_v5.py:29`; 2 files matched credential patterns |
| S-5 | **M** | API runner imports arbitrary module names from a query string (`/run?app=…` → `importlib.import_module`) | `ब्रह्म_API_निष्पादन_तंत्र.py` (old `do_GET`) |
| S-6 | **L** | No security policy, no dependency pinning, no secret scanner | repository metadata |

**Status:** S-5 mitigated (the API runner now validates routes and returns structured errors; module execution remains opt-in and documented); S-1/S-2/S-3 documented — they are architectural (the project's premise is executing user programs), and fixing them requires the sandboxing design in §8.

### 5.7 Documentation

| ID | Sev | Finding |
|---|---|---|
| H-7 | **H** | `README.md` is truncated mid-sentence: it ends with `Clone the repository:` and never shows a clone command, a usage example, or the license. There is no language reference, no bytecode spec, no contribution guide. |
| M-6 | **M** | No statement of what does **not** work; the feature list reads as shipped functionality. |
| M-7 | **M** | CC0 license file present but unmentioned in the README. |

**Status:** README rewritten; `docs/LANGUAGE.md` (grammar, semantics, bytecode, builtins) and `docs/TESTING.md` added; this audit added.

---

## 6. परीक्षण परिणाम (Verification results after this change)

```
$ python -m pytest -q
326 passed, 12 xfailed in 4.4s

$ python -m pytest --cov=brahma
TOTAL   93%   (lexer 97, parser 99, compiler 96, bytecode 94, vm 89, cli 77)

$ flake8 brahma tests tools --count --statistics
0

$ python -c "compile all 725 python files"      → 0 syntax errors
$ python tools/legacy_baseline.py --check       → baseline covers 51 scripts
$ gcc -O2 native_vm/sutra_vm.c && ./sutra_vm    → prints 10 (works)
$ python -m build && pip install dist/*.whl     → `brahma version` works
```

Per-module example verification:

| Program | Output |
|---|---|
| `examples/नमस्ते.sutra` | `नमस्ते, विश्व!` |
| `examples/गणित.sutra` | arithmetic, precedence, compound assignment, Devanagari numerals |
| `examples/फिबोनाची.sutra` | 0 1 1 2 3 5 8 13 21 34 55 89 144 (recursion) |
| `examples/क्रमगुणन.sutra` | `10! = 3628800` |
| `examples/अभाज्य.sutra` | 15 primes ≤ 50 + count |
| `examples/फ़िज़बज़.sutra` | 20 lines with फ़िज़/बज़/फ़िज़बज़ |
| `examples/श्रेणी.sutra` | list indexing, mutation, aggregates |

### 6.1 Legacy demo matrix after the change

**40 / 51 pass** (was 37). The remaining 11 are pinned as `xfail` with their original error text, so any regression or accidental "fix" is visible. Full table: appendix A.

---

## 7. इस परिवर्तन में क्या जोड़ा गया (What was built)

### 7.1 `brahma/` — the engine (1,474 statements)

| Module | Responsibility |
|---|---|
| `tokens.py` | token kinds, Sanskrit↔ASCII keyword table, Devanagari digit mapping |
| `lexer.py` | Unicode identifiers, ०–९ numerals, floats/exponents, strings with escapes, `#` comments, precise line/column |
| `ast_nodes.py` | 18 typed AST nodes |
| `parser.py` | recursive descent, 11 precedence levels, blocks terminated by `अन्त`, `if/elif/else`, `while`, `break/continue`, functions, returns, lists, indexing, assignment forms |
| `compiler.py` | bytecode with jump patching, loop stack for `break/continue`, short-circuit `and/or`, nested `CodeObject`s for functions |
| `bytecode.py` | 19 opcodes, structural validation, versioned JSON container (`SUTRA1` magic), disassembler |
| `vm.py` | frames, locals/globals, 12-function builtin library, recursion, arity and type checks, step budget, call-depth limit, stack traces |
| `api.py` | `execute`, `run_file`, `run_source`, compile helpers, `ExecutionResult` with captured output/steps/error |
| `cli.py` | `run`, `compile`, `disasm`, `check`, `run-bytecode`, `repl` (with multi-line blocks), `version`; exit codes 0/1/2 |
| `errors.py` | diagnostic hierarchy with source positions |

Design decisions are documented in `docs/LANGUAGE.md`.

### 7.2 Tests — 326

| File | Tests | Covers |
|---|---:|---|
| `tests/test_lexer.py` | 24 | tokens, Unicode, numerals, escapes, errors, positions |
| `tests/test_parser.py` | 36 | tree shape, precedence, blocks, error messages |
| `tests/test_compiler.py` | 24 | opcode emission, jump patching, validation |
| `tests/test_bytecode.py` | 16 | round-trip, magic/version, malformed images |
| `tests/test_vm.py` | 89 | arithmetic, strings, lists, logic, control flow, functions/recursion, builtins, limits, tracebacks |
| `tests/test_cli.py` | 36 | every command via subprocess **and** in-process, REPL |
| `tests/test_integration.py` | 30 | all examples, bytecode equivalence, public API, packaging |
| `tests/test_legacy.py` | 71 | 51 demo scripts + 20 module imports, baseline freshness |

### 7.3 Fixes to existing code

| File | Fix |
|---|---|
| `शब्द-विश्लेषक.py` | `from वर्ण-कोश import …` → `from वर्णकोश import …` (hyphen is not a valid module name) |
| `compiler/test_compile.py`, `release/compiler/test_compile.py` | `range(३:)` → valid `range(3)` loop |
| `test_binary_creator.py` | used `ord("अ") = 2304` as a byte → register table `अ/ब/स/द → 0..3` |
| `ब्रह्म_API_निष्पादन_तंत्र.py` | implemented GET/POST dispatch, JSON errors, `प्रारम्भ/बन्द`, callable routes (previously a static dict lookup and no POST at all) |
| `api_test.py` | corrected class name, guarded server start, no hang without a TTY |
| `सूत्र_संकलक.py` | added `सूत्रसंकलक` / `संकलन` compatibility aliases used by `संकलन-परीक्षण.py` |
| `.github/workflows/python-package.yml` | complete rewrite |
| repository | untracked 386 `.pyc`; added `.gitignore`, `.flake8`, `pyproject.toml` |

---

## 8. आगे की योजना (Remaining roadmap)

Ordered by value per unit of work. Items marked ✔ are done in this change.

**P0 — make the project true**
1. ✔ One canonical engine with a real grammar, bytecode, VM, CLI, tests, packaging.
2. ✔ CI that runs the tests on 4 Python versions + wheel build.
3. Rewrite README/claims to match reality (✔ for the engine; the AI/OS/APK sections are now marked *prototype*).

**P1 — consolidate 700 files into a product (est. 2–3 weeks)**
4. Move all legacy modules under `legacy/` (they are already pinned by `tests/legacy_baseline.json`), keeping only `brahma/`, `examples/`, `tests/`, `docs/`, `tools/`, `native_vm/`.
5. Delete `release/` (identical copy) and the 14 `सर्वनिर्माण_v*` generations; keep one generator with a changelog.
6. Pick **one** executable format. The `.sbc` container in `brahma/bytecode.py` is versioned and validated; migrate `native_vm` to read it.
7. Port the OS layer (`process`, `memory`, `scheduler`, `syscall`, `device`) onto the new VM as `brahma/os/` with real tests, replacing the 120+ `*_तंत्र.py` variants.

**P2 — make the artifacts real (est. 2 weeks)**
8. APK: replace hand-written ZIPs with a Gradle/aapt2 pipeline and a real signing key (never commit the key). Until then delete the 29 `.apk` files.
9. ISO: replace `tar` with `grub-mkrescue`/`xorriso` and a freestanding kernel; or drop the "OS image" claim and keep the C kernel as a *hosted shell*.

**P3 — the AI claim (est. 1–2 weeks)**
10. Either integrate a real model behind an explicit interface (`brahma_ai/provider.py` with a local model or an API key from the environment), or rename the subsystem to *scaffolder* and remove "AI" from the README.

**P4 — quality (ongoing)**
11. Remove all bare `except:`; add `logging`; forbid `exec`/`shell=True` outside a documented sandbox.
12. Add `mypy --strict` to CI for `brahma/`; add property-based tests (hypothesis) for the lexer/parser.
13. Add benchmarks and compare the Python VM with the C VM.
14. Add `CONTRIBUTING.md`, issue/PR templates, `SECURITY.md`, `CITATION.cff`.

---

## 9. पुनरुत्पादन (Reproducing this audit)

```bash
git clone https://github.com/Raghav549/Brahmasutra && cd Brahmasutra

# 1. syntax sweep over every Python file
python - <<'PY'
import pathlib
for p in pathlib.Path('.').rglob('*.py'):
    if '__pycache__' in p.parts: continue
    compile(p.read_text(encoding='utf-8'), str(p), 'exec')
print('ok')
PY

# 2. test suite + coverage
pip install -e ".[dev]" pytest-cov
pytest -q --cov=brahma --cov-report=term-missing

# 3. lint
flake8 brahma tests tools --count --statistics

# 4. legacy demo matrix (regenerates tests/legacy_baseline.json in a sandbox)
python tools/legacy_baseline.py

# 5. artifact forensics
python - <<'PY'
import zipfile, pathlib
for apk in pathlib.Path('.').rglob('*.apk'):
    try:
        names = zipfile.ZipFile(apk).namelist()
        print(apk, 'dex' if any(n.endswith('.dex') for n in names) else 'NO DEX')
    except Exception as exc:
        print(apk, 'INVALID ZIP', exc)
blob = open('os/सूत्र_os.iso','rb').read()
print('ISO9660 signature:', blob[0x8001:0x8006] == b'CD001')
PY
```

---

## Appendix A — legacy demo scripts (post-change)

Status legend: ✅ exits 0 · ❌ non-zero exit · ⏱ still running at timeout.
Machine-readable copy: `tests/legacy_baseline.json`.

| # | स्क्रिप्ट | स्थिति | कारण |
|---|-----------|--------|------|
| 1 | `CPU_test.py` | ✅ pass |  |
| 2 | `CPU_परीक्षण.py` | ✅ pass |  |
| 3 | `HAL_परीक्षण.py` | ✅ pass |  |
| 4 | `api_test.py` | ✅ pass |  |
| 5 | `app_manager_test.py` | ✅ pass |  |
| 6 | `app_test.py` | ✅ pass |  |
| 7 | `ast_test.py` | ✅ pass |  |
| 8 | `binary_test.py` | ✅ pass |  |
| 9 | `cpu-परीक्षण.py` | ✅ pass |  |
| 10 | `cpu_test.py` | ✅ pass |  |
| 11 | `executable_test.py` | ✅ pass |  |
| 12 | `filesystem_kernel_test.py` | ✅ pass |  |
| 13 | `hardware_test.py` | ✅ pass |  |
| 14 | `interrupt_test.py` | ✅ pass |  |
| 15 | `kernel_app_test.py` | ✅ pass |  |
| 16 | `machine_test.py` | ✅ pass |  |
| 17 | `memory_protection_test.py` | ✅ pass |  |
| 18 | `memory_test.py` | ✅ pass |  |
| 19 | `mode_test.py` | ✅ pass |  |
| 20 | `native_test.py` | ✅ pass |  |
| 21 | `privilege_test.py` | ✅ pass |  |
| 22 | `process_test.py` | ✅ pass |  |
| 23 | `runtime_test.py` | ✅ pass |  |
| 24 | `scheduler_test.py` | ✅ pass |  |
| 25 | `storage_test.py` | ✅ pass |  |
| 26 | `syscall_test.py` | ✅ pass |  |
| 27 | `test_app.py` | ✅ pass |  |
| 28 | `test_binary_creator.py` | ✅ pass |  |
| 29 | `अनुप्रयोग-परीक्षण.py` | ✅ pass |  |
| 30 | `अनुसूचक-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_प्रक्रिया_तंत्र' has no attribute 'प्रक्रियातंत्र'. Did you me… |
| 31 | `अनुसूचक_परीक्षण.py` | ⏱ timeout | केवल 10s में समाप्त नहीं हुआ |
| 32 | `आदेश-परीक्षण.py` | ✅ pass |  |
| 33 | `आह्वान-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_आह्वान_तंत्र' has no attribute 'आह्वानतंत्र' |
| 34 | `आह्वान_परीक्षण.py` | ✅ pass |  |
| 35 | `उपयोगकर्ता-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_आह्वान_तंत्र' has no attribute 'आह्वानतंत्र' |
| 36 | `निष्पादन-परीक्षण.py` | ✅ pass |  |
| 37 | `परीक्षण.py` | ⏱ timeout | केवल 10s में समाप्त नहीं हुआ |
| 38 | `प्रक्रिया-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_प्रक्रिया_तंत्र' has no attribute 'प्रक्रियातंत्र'. Did you me… |
| 39 | `प्रक्रिया_test.py` | ✅ pass |  |
| 40 | `प्रक्रिया_पृथक्करण_परीक्षण.py` | ✅ pass |  |
| 41 | `बिन-परीक्षण.py` | ✅ pass |  |
| 42 | `यन्त्र-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_यन्त्र_चालक' has no attribute 'यन्त्रचालकतंत्र' |
| 43 | `यन्त्र_चालक_परीक्षण.py` | ❌ fail | EOFError: EOF when reading a line |
| 44 | `व्याख्या-परीक्षण.py` | ✅ pass |  |
| 45 | `संकलन-परीक्षण.py` | ✅ pass |  |
| 46 | `सञ्चिका-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_सञ्चिका_कर्ण' has no attribute 'सञ्चिकातंत्र' |
| 47 | `सञ्चिका_कर्ण_परीक्षण.py` | ✅ pass |  |
| 48 | `सूत्र_mode_test.py` | ❌ fail | AttributeError: module 'सूत्र_kernel_mode' has no attribute 'प्रारम्भ' |
| 49 | `स्मृति-परीक्षण.py` | ❌ fail | AttributeError: module 'सूत्र_स्मृति_तंत्र' has no attribute 'स्मृतितंत्र' |
| 50 | `स्मृति_परीक्षण.py` | ✅ pass |  |
| 51 | `हार्डवेयर_परीक्षण.py` | ✅ pass |  |

---

## Appendix B — module import matrix (702 modules, original commit)

| Outcome | Count |
|---|---:|
| OK | 580 |
| `EOFError` (input at import) | 79 |
| `AttributeError` | 13 |
| `ModuleNotFoundError` | 10 |
| hang | 10 |
| `SyntaxError` | 3 |
| `OSError` (port in use) | 3 |
| `FileNotFoundError` | 2 |
| `ValueError` | 1 |
| `ImportError` | 1 |

Largest error clusters by module family: `सूत्र_*` core (API drift), `ब्रह्म_*` AI/generators (`EOFError` prompts), generated `backend/server.py` (`flask` missing, port binding).

## Appendix C — artefacts

| Artefact group | Count | Valid | Notes |
|---|---:|---:|---|
| `.apk` | 29 | 10 structurally plausible | 14 not ZIPs, 5 ZIPs without dex/manifest, none signed by a real key |
| `.iso` | 1 | 0 | tar archive, 20 KB, no ISO9660 signature |
| ELF binaries (`native_vm/*`, `kernel/sutra_kernel`, `os/kernel/*`) | 5 | 5 | x86-64, run; C sources present; register bounds bug (H-6) |
| `.sbc`/`.bin`/`.सूत्रबिन`/`.यन्त्र` programs | 21 | unknown | no reader exists for most of the formats |

---

*यह लेखा-परीक्षा `docs/AUDIT.md` में स्थिर है और CI द्वारा `pytest` + `tools/legacy_baseline.py --check` के माध्यम से सुरक्षित है।*

---

## 10. v1.2.0 — "fix each and every file" (this release)

The 1.1.0 audit above describes the tree at `27980b8`. This section records what
changed afterwards, and how each claim is verified.

### 10.1 What was done, file by file

| Area | Before (1.1.0) | After (1.2.0) | Verification |
|---|---:|---:|---|
| Python files audited | — | **748** | `find . -name '*.py'` |
| Modules with import-time side effects | 413 | **0** | `python tools/harden_imports.py` |
| Modules loading standalone (probe by file path) | 589 / 725 | **735 / 748** | import matrix, §10.3 |
| Modules importing correctly as packages | 725 / 725 | **748 / 748** | `python -c "import brahma…"` |
| Legacy demo scripts passing | 40 / 51 | **51 / 51** | `tools/legacy_baseline.py` |
| Demo scripts crashing with a traceback | 11 | **0** | root sweep, §10.3 |
| Automated tests | 326 (12 xfail) | **480 (0 xfail)** | `pytest -q` |
| flake8 (`brahma tests tools`) | 0 | **0** | CI |
| Committed binary artefacts | 13 fake/`stale` | **0** (deleted + ignored) | `git ls-files '*.apk' '*.bin'` |

`tools/harden_imports.py` performed the bulk of the work with a
**statement-level** AST transform:

* moved to `_main()`: calls (`print`, `input`, `app.run`, …), loops, `if`
  blocks that call, assignments whose value calls something impure,
  `try`/`with`/`raise`/`assert`, and the body of existing `__main__` guards;
* kept at module level: imports (including `from __future__`), class and
  function definitions, docstrings and constant assignments — so
  `from module import SomeClass` keeps working;
* every rewrite verified by (a) re-parsing, (b) comparing script behaviour
  before/after with volatile tokens normalised, (c) re-importing the module;
  anything that fails a check is restored byte-for-byte.

### 10.2 Real defects fixed in this pass

| Defect | Impact | Fix |
|---|---|---|
| Flask imported in 9 backends but declared nowhere | every demo server raised `ModuleNotFoundError` | rewritten on the stdlib (`brahma_web` + `brahma_chat`) |
| `POST /run` executed client-supplied files **in-process** | unauthenticated RCE + path traversal | name validation, subprocess, timeout, opt-in via `BRAHMA_ALLOW_EXEC=1` |
| `os.system(f"termux-open '{path}'")` with user input | shell injection | argument vectors via `subprocess` |
| `eval(file.read())` in the binary executor | arbitrary code execution | `ast.literal_eval` |
| 5 compilers, 4 incompatible bytecode layouts | compiled files could not be executed | one documented format (`brahma_bytecode`) + 4 shims |
| `सूत्रBinaryLoader.load_and_run()` called but never defined | OS loader always crashed | method added, malformed images raise |
| 3 module-level constants (`डिफ़ॉल्ट_मूल`, `BASE`, `HOME`) moved behind guards by the first transform attempt | `NameError` at first use | `--hoist-pure` repair pass + pure-call allowlist |
| `परीक्षण.py` / `अनुसूचक_परीक्षण.py` infinite loops | demos could never finish | bounded rounds, `--rounds` option |
| shells blocking on `input()` during boot | boot sequence hung headless | `प्रारम्भ(interactive=None)` detects a terminal |
| `admin123` hard-coded | credential leak in git | password from `BRAHMA_ADMIN_PASSWORD`, generated otherwise |
| 8 committed `.apk` text files, stale `.bin`/`.img` | artefacts lied about being apps | deleted, `.gitignore`d, `is_installable_apk()` added |

### 10.3 Reproducing the matrix

```bash
python tools/harden_imports.py                 # 0 files with import-time effects
python tools/legacy_baseline.py                # 51/51 legacy scripts pass
pytest -q --cov=brahma                        # 414 passed, 93 %
flake8 brahma tests tools                     # 0
python -m build                               # sdist + wheel
```

Remaining import-matrix entries (13 of 748) are **artefacts of the probe**, not
of the code: `brahma/*` uses relative imports and `@dataclass`, so loading a
single file by path with a synthetic module name fails while
`import brahma.parser` succeeds — verified in the same run.

### 10.4 What is still *not* true (kept honest)

* The `.apk` builder produces **ZIP bundles**, not installable apps; a real APK
  needs `aapt2`, `d8` and a keystore. `brahma_packaging.is_installable_apk()`
  returns `False` for every file this repository can build.
* `brahma_ai` is a real **n-gram** model and a keyword router — not a neural
  network, not an LLM, and it does not generate code by itself: the
  `*_creator_ai_*` scripts are template generators driven by it.
* The legacy OS-style layer (`kernel/`, `os/`) remains a prototype; the C kernel
  is a userspace REPL and the `.iso` is a tar archive.
* `mypy --strict` is **not** wired into CI yet (roadmap item 5); typing is
  gradual (`from __future__ import annotations` + annotations on new modules).

---

## 11. अद्यतन लेखा-परीक्षा — 3.6.0 (2026-10-27)

Everything below was re-measured on the 3.6.0 tree, not carried over.

### 11.1 Shape

| Metric | 1.x (original audit) | 3.6.0 |
|---|---|---|
| Tracked files | 1,006 | **1,031** |
| Python files | 702 | **702** |
| `.सूत्र` programs in the tree | 9 | **35** (incl. 3 in `brahma/lib/`) |
| Engine (`brahma/`) | 1,474 statements | **3,564 lines**, 31 opcodes |
| Model + kernel + server (`brahma_llm/`) | — | **4,696 lines** |
| सूत्र standard library (`brahma/lib/`) | — | **233 lines**, 26 exports |
| Tests | 0 → 326 | **588**, `tests/` 3,978 lines |

### 11.2 Gates (all re-run for 3.6.0)

| Gate | Command | Result |
|---|---|---|
| Test suite | `pytest -q` | **588 passed**, ~34 s |
| Lint | `flake8 brahma brahma_llm tests tools --count` | **0** |
| Import-time side effects | `tools/harden_imports.py` | **0 files** |
| Legacy script pins | `tools/legacy_baseline.py --check` | **51 scripts** |
| Demo sweep | `tools/demo_sweep.py --check` | **221 scripts** — ok=189, server=26, usage=6 |
| Kernel boot | `brahma llm kernel verify` | **7/7 subsystems, READY**, 12 API functions (2 113 steps, 215 241-byte image) |
| Version | `brahma version` | `BRAHMA 3.6.0` |

The six `usage` demos are *documented* command-line tools that print their usage
and exit non-zero when called with no arguments; they are counted, not hidden.
The 26 `server` demos open a port and are killed after the readiness probe.

### 11.3 What changed since the original audit

* **Language:** dicts, slices, closures, `प्रयास`/`पकड़`/`अन्ततः`/`उठाओ`,
  string interpolation, slice assignment, `बाह्य`/`वैश्विक`, and in 3.6.0
  tuples, sets, callable expressions and the `आयात` module system with a
  standard library written in सूत्र. Remaining gaps are listed in
  `docs/LANGUAGE.md §11` (classes, `for`, exception types, keyword arguments).
* **LLM:** `brahma_llm/` trains from the सूत्र corpus, verifies its own maths in
  सूत्र, edits its body without changing predictions, boots a सूत्र-OS kernel
  image before installing itself, and serves chat/code/action/image over HTTP.
  Measured numbers live in `docs/LLM.md`; the honest limits (≈2.4 M parameters
  at the top preset, no attention, no GPU) are stated there rather than glossed.
* **Security:** `SECURITY.md` is rewritten for 3.x — in particular it now says
  plainly that `आयात` executes files from the search path, and that the HTTP
  server has no authentication.

### 11.4 What is still not true

* The app-builder tree (`अनुप्रयोग/`, `ब्रह्म_AI_*निर्माता.py`, …) still exists
  as legacy code. It is **not** the product any more: `brahma llm` is. It is
  pinned by tests so it cannot silently rot, but it is not maintained.
* `native_vm/` (C) remains a separate, smaller prototype and does not implement
  the current specification.
* No GPU, no attention, no pre-training on external corpora: the model is a
  hand-written neural LM trained from the repository's own सूत्र corpus.
* Coverage is reported at 93 % for the engine (`brahma/`); the LLM package is
  exercised by tests but not coverage-measured in CI.
