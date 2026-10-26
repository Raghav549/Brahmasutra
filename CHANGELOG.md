# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [3.0.0] — 2026-10-27

**"ब्रह्म-LLM is the application" release.**  The app builder is gone.  ब्रह्म
answers chat, writes सूत्र code, executes it, explains it and renders images on
one dependency-free server; the सूत्र-OS kernel is a complete six-subsystem
program; the language gained dictionaries, slicing and 26 builtins.

### Added

* **`brahma_llm/agent.py`** — `BrahmaAgent` with real capabilities, routed by
  intent: `chat`, `code` (candidates are **ranked by the model's own loss**, then
  compiled and executed), `run`, `explain` (structural, deterministic), `image`,
  `status`, `help`.  Every reply carries a trace of what executed.
* **`brahma_llm/server.py`** — `brahma llm serve`: `/`, `/status`, `/kernel`,
  `/chat`, `/generate`, `/run`, `/explain`, `/image`, optional `/train`.
* **`brahma llm ask` / `chat` / `image` / `serve`** — the same agent from the CLI.
* **`brahma_llm/image.py`** — real PNGs from the model's own सूत्र program plus
  its next-token distribution (zlib/struct only; procedural, and labelled so).
* **सूत्र-OS rewritten** (`brahma_llm/os_kernel.py`): memory allocator, process
  table, round-robin scheduler, syscall table, in-memory filesystem and
  interrupt handling — 5/5 self-tests, 1 723 steps, a nine-function kernel API
  dictionary, booted and verified on the project's VM.
* **`mission` now ends by serving itself**: the trained model is started on a
  real port and `/status`, `/kernel`, `/chat`, `/run` and `/image` are
  smoke-tested (`smoke_ok`).  `--resume`, `--continuous`,
  `--target-perplexity` and `--max-generations` make it a loop.
* **Language**: dict literals/indexing/nested assignment, slices `x[a:b]`,
  multi-line literals inside brackets, and new builtins — `विभाजन`,
  `प्रतिस्थापन`, `त्रिम`, `बड़े`, `छोटे`, `खोज`, `दोहराओ`, `क्रम`, `उलटा`,
  `हटाओ`, `सम्मिलित`, `विस्तार`, `गिनती`, `स्थान`, `योगफल`, `सूची`, `कुंजियाँ`,
  `मान`, `समाविष्ट`, `हटाओ_कुंजी`, `तालिका`, `वर्गमूल`, `प्रकार`, `गोल`,
  `मिलाओ`.
* **Scale presets** `xlarge` (314 240), `huge` (886 272) and `brahma`
  (**2 411 008** parameters, instantiated and counted).  Measured 1-epoch runs:
  `large` 115 287 params in 21.7 s; `xlarge` 254 919 in 50.3 s; `huge` 558 903
  — with *worse* perplexity, which is the honest result without more data.
* 23 new tests (agent, image, HTTP surface, resume/continuous, tables/slices/builtins) — **483**.

### Changed

* `brahma_llm/app_builder.py` **removed**; `कृत्रिमबुद्धि/सूत्र_अनुप्रयोग_निर्माता.py`
  now drives the agent and points at `brahma llm serve`.
* `brahma_chat` `/llm` also returns the last mission summary; `brahma llm info`
  prints it.
* Header values that are not latin-1 are escaped in `brahma_web` instead of
  killing the request (found by serving Devanagari origin tags).

### Removed

* The 16 committed `सर्वनिर्माण_v12…v27` output trees, the duplicated `release/`
  copy, and five truncated `*.py.` / `*.py.y` files (109 files).  Gates after
  removal: legacy baseline 51/51, demo sweep 221 scripts / 0 failures.

### Honest scope

The largest model here is 2.41 M parameters (instantiated) / 558 903 (trained one
epoch).  This is not the largest or most powerful LLM in existence and the docs
say so; what is claimed is that the entire chain — सूत्र language → VM →
bytecode → kernel → trainer → self-editor → agent → HTTP → PNG — is implemented
here, from scratch, and runs.

## [2.1.0] — 2026-10-26

### Added

* **`brahma llm mission --target TEXT`** — one command for the whole cycle:
  autonomous training, body edits, the model **writing its own kernel body**
  (accepted only if the composed kernel boots; otherwise the shipped kernel is
  reinstalled and the report says so), and a generated app whose HTTP endpoints
  are smoke-tested. Everything lands in `$BRAHMA_HOME/mission/mission.json`.
  Measured: 2.9 s, perplexity 15.313 → 14.006, `origin = model`, app smoke `ok`.
* 4 mission tests (whole cycle, opt-out flags, boot harness, broken-kernel
  fallback) — 460 tests in total.

### Fixed

* A generated kernel that fails to compile now produces a **rejected edit**
  instead of aborting the run (`SelfEditor.try_os` catches compile/boot errors).

## [2.0.0] — 2026-10-26

**"ब्रह्म-LLM" release.**  The language, the VM, the kernel and the application
builder are now driven by a language model that lives in this repository, is
trained from scratch in the standard library, edits its own weights and rebuilds
its own OS image — with every claim backed by a test or a reproducible command
(see `docs/LLM.md`).

### Added

* **`brahma_llm` package** — a complete, dependency-free language-model stack:
  * `tokenizer.py` — akṣara-level, Devanagari-aware tokenizer with reversible
    decoding and frequency-pruned vocabulary;
  * `model.py` — `NgramLM` (Jelinek–Mercer) and `NeuralLM` (embedding → tanh →
    softmax) with **hand-written backpropagation**, Adam, size presets and JSON
    checkpoints; gradients verified against central differences (2e-11);
  * `programs.py` — a सूत्र program generator whose candidates are **executed**
    before they may enter the training corpus, plus repository corpus loading;
  * `trainer.py` — the target-driven autonomous loop: generate → validate →
    train → measure → keep-best → grow → stop on threshold/patience/budget;
  * `selfedit.py` — prediction-preserving weight surgery (grow/prune hidden
    units), gated OS reinstall, and an audit log of every attempt;
  * `kernel.py` — the **SUTRAOS** kernel as a सूत्र program: compile → pack
    (`"SUTRAOS" + version + length + bytecode`) → boot → verify → install;
  * `sutra_kernel.py` — exp/tanh/softmax/forward-pass written **in सूत्र** and
    executed on the project VM; equal to the Python path within 8.3e-16;
  * `app_builder.py` — the app builder, now LLM-driven: model writes the सूत्र
    logic, the builder runs it, generates a stdlib server + UI, and smoke-tests
    the HTTP endpoints before reporting success;
  * `cli.py` — `brahma llm info|corpus|train|generate|complete|chat|autotrain|
    evolve|kernel|build-app|sutra-math|bench`.
* **`brahma llm …`** wired into the main CLI (`brahma/cli.py`).
* **LLM endpoints in `brahma_chat`** — `/llm`, `/llm/generate` and `/llm/run`
  (the last one compiles and runs posted सूत्र source on the VM, with a
  20 000-character source cap and a 100 000-step limit).
* **Real SUTRAOS image format** — `pack_image`/`unpack_image` in
  `brahma/bytecode.py`, shared by `brahma_bytecode` and `brahma_llm.kernel`.
* **40 new tests** (`tests/test_llm.py`) — 456 in total.

### Changed

* **`कृत्रिमबुद्धि/सूत्र_अनुप्रयोग_निर्माता.py`** — the old builder wrote a fixed
  program in a dead opcode dialect and printed "निर्मित"; it now delegates to
  `brahma_llm.app_builder` and returns a manifest with a passing smoke test.
* **`कृत्रिमबुद्धि/सूत्र_पूर्ण_स्वचालित_निर्माता.py`** — "compilation" used to
  copy UTF-8 text to `.सूत्रबिन` and "execution" printed the source; now the
  सूत्र source is compiled to real bytecode (`.sbc`), executed on the VM and can
  be disassembled.
* **`kernel/kernel_engine.py`** — was `exec()`-ing arbitrary files; it is now a
  real shell for the SUTRAOS kernel (`boot`, `verify`, `run FILE.sutra`,
  `memory`), and it compiles `.sutra` programs instead of executing Python.
* **`सूत्र_boot_image_builder.py`** — writes and verifies the real image instead
  of a 10-byte header around a stray file.
* **`कृत्रिमबुद्धि/सूत्र_स्वायत्त/स्वविकास_कृत्रिमबुद्धि.py`** — generated modules
  go to the data directory (`BRAHMA_HOME`) instead of the current working
  directory, and their demos terminate (they used to loop forever).
* **Trainer annealing** — warm rounds decay the learning rate (0.6×), which
  turned an oscillating loop (12.7 → 13.0 → 16.2 perplexity) into a monotone one
  (10.4 → 9.7 → 9.2 → 9.0).

### Removed

* 13 generated demo files that the self-growing AI demos had dropped into the
  checkout, plus the committed `कृत्रिमबुद्धि/मॉड्यूल_5287.py`; `.gitignore` now
  covers them.
* The `exec()`-based "kernel" and the fake `सूत्र.img` builder.

### Fixed

* **Sub-directory demos: 49 failures → 0.** `tools/demo_sweep.py` (new) runs the
  264 scripts outside `tests/`, `brahma/` and `brahma_llm/`. Fixed: 17 modules
  that could not import their own package when executed directly
  (`vm/`, `runtime/`, `desktop/`, `engine/apk_*`, `ब्रह्म_AI_अनुप्रयोग/*` now add
  the repository root to `sys.path`), 11 demos that raised `EOFError` or looped
  forever without a terminal (they use a headless-safe `_इनपुट` that exits after
  the second EOF), and two programs with working-directory-relative paths
  (`द्विआधारी/निष्पादन_परीक्षण.py`, `संकलक/संकलक_परीक्षण.py`). Current result:
  232 ok, 26 servers (blocking by design), 6 usage errors, **0 failures**.
* `NeuralLM` gradients (verified numerically), Adam state migration across
  weight surgery, and `shrink_hidden` indexing (`W1` rows are hidden units).
* `ब्रह्म_API_निष्पादन_तंत्र` now sets `allow_reuse_address`, so a repeat run no
  longer fails with `Address already in use` while the previous socket sits in
  `TIME_WAIT`; the legacy baseline was regenerated after that fix (a stale
  record had captured the collision as a real failure).
* Import-time side effects in the new demos (data directories are created
  lazily) — `tools/harden_imports.py` still reports **0** files.

## [1.2.0] — 2026-10-26

**"Fix each and every file" release.**  Every one of the 748 Python files in the
repository was audited, made import-safe and made to behave honestly; every
legacy demo now passes.  Nothing in this release is aspirational: each claim
below is backed by a test or by a reproducible command.

### Added

* **`brahma_web`** — a dependency-free HTTP framework (`App`, `Request`,
  `Response`, routing with path parameters, JSON in/out, CORS, threaded server,
  `start()`/`shutdown()` for tests).  Replaces the undeclared Flask dependency.
* **`brahma_chat`** — one shared chat/authentication backend for the eight demo
  servers: PBKDF2-HMAC-SHA256 password hashes with per-user salt, tokens from
  `secrets`, atomic JSON writes, administrator password from
  `BRAHMA_ADMIN_PASSWORD` (generated and printed once if unset — the hard-coded
  `admin123` is gone).
* **`brahma_bytecode`** — a single documented bytecode format plus assembler,
  disassembler, interpreter and boot-image packer (`SUTRAOS` header).  The five
  former compilers now all emit this one format, so a compiled `.यन्त्र` file is
  guaranteed to be executable.
* **`brahma_ai`** — a real, local n-gram language model (`MarkovModel`: train,
  generate, perplexity, save/load) and a transparent `PromptRouter` that selects
  an application template and always reports the rule that fired.
* **`brahma_cli`** — shared entry-point helper: closed stdin becomes exit code 2
  with a clear message, Ctrl-C becomes 130, genuine errors still show a
  traceback.
* **`brahma_paths`** — one data-root policy (`BRAHMA_HOME`, else `~/सूत्र-तंत्र`)
  replacing hard-coded Termux paths.
* **`brahma_packaging`** — honest Android bundles: builds a ZIP archive, states
  that it is not an APK, and `is_installable_apk()` verifies manifest/DEX
  signatures so the project can never again label a text file `.apk`.
* **`brahma_templates`** — self-contained, stdlib-only server templates used by
  the generators (they may write outside the repository, so they cannot import
  it).
* **`tools/harden_imports.py`** — the AST tool used for this pass: classifies
  import-time side effects, moves only *effects* behind `_main()` (classes,
  functions and constants stay at module level), verifies behaviour
  before/after, restores any file it cannot prove equivalent, and supports
  `--apply`, `--verify`, `--hoist-pure`, `--wrap-main` and `--json`.
* **90 new tests** (`tests/test_web_stack.py` plus two invariants in
  `tests/test_legacy.py`) covering the web stack, chat backend, bytecode format,
  CLI helper, paths, generators, packaging, the AI model, and the rule that no
  module may have import-time side effects or third-party imports — 416 tests in
  total.

### Fixed

* **419 files** rewritten: every module that printed, prompted, looped or served
  on import now exposes `_main()`; importing it is side-effect free.
  `625` import-time side effects were removed; 735/748 modules load standalone
  and all 748 import correctly (`brahma/*` are package-relative by design).
* **All 51 legacy demo scripts pass** (previously 40 passed, 9 failed, 2 hung).
  The two infinite loops are now bounded (`परीक्षण.py`, `अनुसूचक_परीक्षण.py`),
  and the shells/repls accept `interactive=False` so boot sequences work
  headless.
* **Nine Flask backends replaced** — `chat_app`, `chat_saas`, `chat_admin_saas`,
  three `..._login_database_api_dashboard` apps and `ब्रह्म_API_स्वचालित_
  निष्पादन.py` — all now run on the standard library.
* **Remote-code-execution endpoint closed** in
  `ब्रह्म_API_स्वचालित_निष्पादन.py`: app names are validated (no separators, no
  `..`), executions run in a subprocess with a timeout, and the whole endpoint is
  disabled unless `BRAHMA_ALLOW_EXEC=1`.
* **Shell injection removed** (`ide.py`, `sutra_bhasha_v2.py`,
  `sutra_bhasha_v3.py`): `os.system(f"…{user input}…")` → argument vectors via
  `subprocess`; `eval()` in `द्विआधारी/सूत्र_द्विआधारी_निष्पादक.py` →
  `ast.literal_eval()`.
* **`सूत्र_यन्त्र_निष्पादक` / `सूत्र-यन्त्र-संकलक` / `सूत्र_मूल_संकलक` /
  `सूत्र_संकलक`** agree on one format; the interpreter raises
  `असेंबली_त्रुटि` instead of `IndexError`.
* **`सूत्र_binary_loader`** — `load_and_run()` exists (it was called but never
  defined, so the OS loader crashed), malformed images raise instead of
  producing nonsense instructions.
* **`सूत्र_boot_simulator`** builds and verifies its image at run time instead of
  depending on two stale committed binaries.
* **`सूत्र_os_loader`**, **`सूत्र_shell_v2/v3`**, **`सूत्र_कर्ण_v2`**,
  **`सूत्र_प्रक्रिया_तंत्र`**, **`सूत्र_यन्त्र_तंत्र`** provide the names the demos
  use (`चलाओ`, `प्रारम्भ`, `सूत्रयन्त्र`, `संकलन`), created lazily so importing
  them stays silent.
* **12 fake binary artefacts deleted** from git (`*.apk` text files, stale
  `.bin`/`.यन्त्र`/`.img`); `.gitignore` now covers generated binaries.
* **Demos that needed input** exit `2` with a one-line explanation instead of an
  `EOFError` traceback; demos that touch the filesystem use `BRAHMA_HOME`.

### Changed

* `pyproject.toml` now ships the nine support modules as `py-modules` and the
  `dev` extra includes `build`.
* Documentation states precisely what is and is not real: the "AI" generators
  are template engines driven by `brahma_ai.PromptRouter` (with a real n-gram
  model available), the "APK" builder produces ZIP archives, and the engine
  remains the supported core.

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
