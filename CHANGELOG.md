# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-10-26

First release of a working, tested BRAHMA engine, produced by a full audit of
the previously untested prototype tree (see `docs/AUDIT.md`).

> The `v1.0.0` tag on this repository predates the audit and points at the
> untested prototype tree. The engine described below is published as `v1.1.0`
> so that the earlier tag and release stay intact and reproducible.

### Added

* **`brahma/` engine** — lexer, recursive-descent parser with 11 precedence
  levels, bytecode compiler with jump patching and nested code objects, stack
  virtual machine with frames/recursion/limits, and structured diagnostics:
  * `brahma/tokens.py`, `brahma/lexer.py` — Unicode identifiers, Devanagari
    numerals (०–९), floats/exponents, strings with escapes, comments, precise
    line/column positions.
  * `brahma/ast_nodes.py`, `brahma/parser.py` — statements
    `let`/`print`/`if`/`elif`/`else`/`while`/`break`/`continue`/`func`/`return`,
    expressions, calls, lists, indexing, compound assignment; parse-time
    validation of `break`/`continue`/`return` placement.
  * `brahma/compiler.py` — 19 opcodes, short-circuit `and`/`or`, loop jump
    patching, function objects.
  * `brahma/bytecode.py` — versioned `.sbc` container (`SUTRA1` magic + JSON),
    full structural validation, disassembler.
  * `brahma/vm.py` — frames, locals/globals, 12 builtin functions, arity/type
    checks, instruction budget, call-depth limit, call-stack traces.
  * `brahma/api.py` — `execute`, `run_source`, `run_file`, `ExecutionResult`.
  * `brahma/cli.py` — `run`, `compile`, `disasm`, `check`, `run-bytecode`,
    `repl` (with multi-line blocks), `version`.
* **7 example programs** in `examples/` (hello, arithmetic, lists, factorial,
  fibonacci, primes, fizzbuzz) — all executed by the test suite.
* **326 tests** in `tests/` covering lexer, parser, compiler, bytecode, VM, CLI,
  examples, public API and the legacy tree; **93 %** statement coverage of the
  engine.
* **Legacy regression matrix** — `tests/legacy_baseline.json` and
  `tools/legacy_baseline.py` record the behaviour of all 51 historical demo
  scripts and 20 curated module imports; working demos are asserted, broken ones
  are pinned as expected failures, and new scripts must be registered.
* **Packaging** — `pyproject.toml` (wheel/sdist, `brahma` console script,
  `.[dev]` extra, pytest and flake8 configuration), `.flake8`, `.gitignore`.
* **Documentation** — `docs/AUDIT.md` (full audit), `docs/LANGUAGE.md`
  (language + bytecode reference), `docs/TESTING.md`, rewritten `README.md`,
  this changelog.

### Fixed

* `api_test.py` / `ब्रह्म_API_निष्पादन_तंत्र.py` — the demo imported a class that
  did not exist; the API runner now supports GET **and** POST, callable routes,
  structured JSON errors, thread start (`प्रारम्भ`) and clean shutdown
  (`बन्द`), and no longer hangs without a TTY.
* `शब्द-विश्लेषक.py` — `from वर्ण-कोश import …` (a hyphen is not a valid module
  name) → `from वर्णकोश import …`.
* `compiler/test_compile.py`, `release/compiler/test_compile.py` — `range(३:)`
  did not parse.
* `test_binary_creator.py` — used `ord("अ") = 2304` as a byte value; now uses the
  documented register table `अ/ब/स/द → 0..3`.
* `सूत्र_संकलक.py` — added the `सूत्रसंकलक` / `संकलन` names used by
  `संकलन-परीक्षण.py`.
* CI workflow — previously ran `pytest` against a tree that could not be
  collected; replaced with five real jobs (lint, syntax sweep, 4-version test
  matrix, packaging, native build) plus the legacy baseline check.

### Changed

* `__pycache__/*.pyc` files (386) are no longer tracked.
* Pytest is scoped to `tests/` (`testpaths`), so demo scripts can never be
  imported by the collector again.
* The README now distinguishes stable, prototype and legacy components instead
  of claiming unfinished subsystems as features.

### Removed

* Nothing was deleted. The legacy tree is preserved for provenance and pinned by
  tests; the audit's roadmap proposes moving it under `legacy/` in a follow-up.

## Legacy history (pre-1.0.0)

The repository previously contained a single commit of ~1,480 files spanning 27
generations of experiments (Sanskrit language prototypes, a C VM, an "OS",
APK generators and template-based app scaffolding). It had no tests, no
packaging, no `.gitignore`, and no working end-to-end language pipeline. See
`docs/AUDIT.md` for the complete assessment.
