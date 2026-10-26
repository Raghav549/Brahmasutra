# सुरक्षा नीति (Security Policy)

## Supported versions

| Version | Supported |
|---|---|
| **3.x** — `brahma/` (engine), `brahma_llm/` (model, kernel, server), `brahma/lib/` (सूत्र standard library) | ✅ |
| 1.x / 2.x engines | ⚠️ superseded — upgrade to 3.6.0 |
| legacy prototype tree (`सूत्र_*.py`, `ब्रह्म_*.py`, `*_तंत्र.py`, `engine/`, `apk/`, `os/`, `अनुप्रयोग/`) | ❌ not supported, kept for provenance |

## Reporting a vulnerability

Please open a private security advisory on GitHub
(<https://github.com/Raghav549/Brahmasutra/security/advisories/new>) rather than a
public issue. Include the version, a minimal reproducer and the impact. We aim to
respond within 7 days.

## Threat model of the engine (`brahma/`)

What a BRAHMA program **can** do:

* compute with numbers, strings, lists, tables, tuples and sets;
* call the builtin library — 88 names (43 builtin functions plus ASCII/Sanskrit
  aliases), all pure: no sockets, no processes, no `eval`, no environment access;
* **read and execute `.सूत्र` files** through `आयात` (3.6.0).  The search path is
  the importing file's directory, the current directory, the installed
  `brahma/lib`, then `BRAHMA_PATH`.  A module body runs once per VM and can
  itself import other modules; circular imports are refused.

Because `आयात` executes files from disk, **a BRAHMA program is as trusted as its
search path**. Run untrusted source the way you would run an untrusted shell
script — inside a container or a throwaway process.

Execution guards:

* instruction budget — default 1 000 000 steps (`--limit`, `step_limit=`);
* call-depth limit — default 500;
* index/type/arity checks on every operation, with source position and a call
  trace in the fault;
* bytecode images (`.sbc`) are validated before execution: format name, version,
  every opcode, every jump target and every nested code object. A malformed image
  raises `BytecodeError` and never executes partially.

These are **robustness guards, not a sandbox**: a hostile program can still burn
its whole instruction budget and grow lists until the process runs out of memory.

## The LLM server and kernel (`brahma_llm/`)

* `brahma-llm serve` binds `0.0.0.0` by default and has **no authentication**;
  it is a local-development server. Do not expose it to the internet. It can
  train models, write checkpoints and **execute BRAHMA programs**
  (`POST /run`, `POST /shell`) with a reduced 200 000-step budget per request.
* `POST /train` writes checkpoints under `$BRAHMA_HOME` (default
  `~/.brahma`); treat that directory as trusted input on the next run.
* `brahma llm selfedit` rewrites files in the repository. It refuses paths
  outside the repository root and keeps a backup, but it is still a
  code-writing tool: review the diff before committing (see `docs/LLM.md §5`).
* The सूत्र-OS kernel (`brahma_llm/os_kernel.py`) runs on the BRAHMA VM, not on
  hardware. It simulates memory, processes, scheduling, syscalls, files and
  interrupts; it cannot touch the host beyond the same `आयात`/file behaviour
  described above.

## Known unsafe code in the legacy tree

The historical prototype contains patterns that must **not** be used in
production and that are absent from the supported engine:

* `exec()` / `eval()` on user-supplied files
  (`kernel/kernel_engine.py`, `द्विआधारी/सूत्र_द्विआधारी_निष्पादक.py`,
  `IDE/सूत्र_IDE.py`, …)
* `os.system()` and `subprocess(..., shell=True)` with interpolated strings
  (`ide.py`, `sutra_bhasha_v2.py`, `ब्रह्म_प्रक्रिया_निष्पादन_कोर.py`)
* an HTTP endpoint that imported a module named by a query parameter
  (`ब्रह्म_API_निष्पादन_तंत्र.py`; the 1.1.0 rewrite validates routes and returns
  structured errors, and module execution stays opt-in)
* generated applications with a hard-coded administrator password
  (`brahma_auto_v5.py`)

Every module in the tree is also checked for *import-time* side effects by
`tools/harden_imports.py` (currently **0** files with side effects), so
`import`-ing a legacy module no longer prints banners, prompts for input or
starts servers.

See `docs/AUDIT.md §5.6` for the full list with file references.
