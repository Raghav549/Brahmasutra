# सुरक्षा नीति (Security Policy)

## Supported versions

| Version | Supported |
|---|---|
| 1.x (`brahma/`) | ✅ |
| legacy prototype tree (`सूत्र_*.py`, `ब्रह्म_*.py`, `*_तंत्र.py`, `engine/`, `apk/`, `os/`) | ❌ not supported, kept for provenance |

## Reporting a vulnerability

Please open a private security advisory on GitHub
(<https://github.com/Raghav549/Brahmasutra/security/advisories/new>) rather than
a public issue. Include the version, a minimal reproducer and the impact. We aim
to respond within 7 days.

## Threat model of the engine (`brahma/`)

* BRAHMA programs **cannot** read or write files, open sockets, start processes,
  or import Python modules. The builtin library is a fixed set of 12 pure
  functions (`docs/LANGUAGE.md §6`).
* Execution is bounded: an instruction budget (default 1,000,000) and a call
  depth limit (default 500) stop accidental runaway programs.
* **These limits are robustness guards, not a security sandbox.** A malicious
  program can still consume CPU up to the budget and memory through list growth.
  If you execute untrusted BRAHMA code, run it in a container or a separate
  process with OS-level limits.
* Bytecode images (`.sbc`) are validated before execution: format name, version,
  opcodes, jump targets and nested code objects. Malformed images raise
  `BytecodeError` and never execute partially.

## Known unsafe code in the legacy tree

The historical prototype contains patterns that must **not** be used in
production, and that are disabled in the supported engine:

* `exec()` / `eval()` on user-supplied files
  (`kernel/kernel_engine.py`, `द्विआधारी/सूत्र_द्विआधारी_निष्पादक.py`,
  `IDE/सूत्र_IDE.py`, …)
* `os.system()` and `subprocess(..., shell=True)` with interpolated strings
  (`ide.py`, `sutra_bhasha_v2.py`, `ब्रह्म_प्रक्रिया_निष्पादन_कोर.py`)
* an HTTP endpoint that imports a module named by a query parameter
  (`ब्रह्म_API_निष्पादन_तंत्र.py`; the 1.0.0 rewrite validates routes and returns
  structured errors, but module execution remains opt-in)
* generated applications with a hard-coded administrator password
  (`brahma_auto_v5.py`)

See `docs/AUDIT.md §5.6` for the full list with file references.
