#!/usr/bin/env python3
"""Make every module in the repository safe to import — without changing its API.

The historical prototype tree runs its demo body at *import* time: ``input()``
prompts, ``while True`` loops, ``app.run()`` servers and banner ``print``s all
fire when a module is imported.  That makes 100+ modules unusable as libraries
and poisons test collection.

This tool performs a **statement-level** rewrite.  Effects are moved, and only
effects — every class, function, import and constant stays at module level, so
``from module import SomeClass`` keeps working:

===============  ========================================================
moved (_main)    ``print``/``input`` calls, loops, ``if`` blocks that call,
                 assignments whose value calls something (``obj = App()``),
                 ``try``/``with``/``raise``/``assert`` bodies, the body of an
                 existing ``if __name__ == "__main__":`` guard
stays put        imports, class/function definitions, literal assignments,
                 docstrings, ``__future__`` imports
===============  ========================================================

Names bound by the moved statements are declared ``global`` inside ``_main()``,
so modules that export objects created in their demo body (for example the
shared ``प्रबंधक = प्रक्रिया_प्रबंधक()`` instance) keep exporting them.

Every rewrite is verified:

1. the file still parses;
2. running it as a script produces the same exit code and output as before
   (timestamps/UUIDs normalised);
3. importing it now works (before: it may not).

Any file that fails a check is restored byte-for-byte.

Usage::

    python tools/harden_imports.py              # report only
    python tools/harden_imports.py --apply      # rewrite + verify
    python tools/harden_imports.py --json p.json
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from typing import List, Optional, Sequence, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
    "tests",
    "tools",
    "examples",
    "docs",
    "brahma",
    "node_modules",
    ".pytest_cache",
    ".hypothesis",
}

THIRD_PARTY = ("flask", "flask_cors", "werkzeug", "requests")

#: Calls that only compute a value.  An assignment whose calls are all in this
#: set is harmless at import time and must stay at module level — moving it
#: would hide the constant from the module's public API.
PURE_CALLS = {
    "expanduser", "expandvars", "abspath", "dirname", "basename", "join",
    "realpath", "normpath", "split", "getcwd", "get", "getenv", "strip",
    "lower", "upper", "replace", "format", "Path", "str", "int", "float",
    "bool", "list", "dict", "set", "tuple", "len", "sorted", "environ",
    # deterministic, side-effect free helpers
    "insert", "compile", "match", "search", "sub", "splitlines", "encode",
    "decode", "getLogger", "namedtuple", "dataclass", "field", "defaultdict",
    "gettempdir", "getpid", "exists", "isfile", "isdir", "listdir", "walk",
    "commonpath", "relpath", "splitext", "items", "values", "keys", "get",
}

_VOLATILE = (
    (re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"), "<uuid>"),
    (re.compile(r"\b[0-9a-fA-F]{8,}\b"), "<hex>"),
    (re.compile(r"\b20\d{2}-\d{2}-\d{2}[ T][0-9:.]+"), "<time>"),
)

BANNER = (
    "# ---------------------------------------------------------------------------\n"
    "# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that\n"
    "# importing this module has no side effects. Classes and functions above stay\n"
    "# at module level, so the module's public names are unchanged.\n"
    "# ---------------------------------------------------------------------------\n"
)


# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------
def _docstring(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _main_guard(node: ast.stmt) -> bool:
    if not isinstance(node, ast.If):
        return False
    return any(isinstance(n, ast.Name) and n.id == "__name__" for n in ast.walk(node.test))


def _is_path_bootstrap(node: ast.Call) -> bool:
    """``sys.path.insert(...)`` — the accepted idiom for script-mode imports.

    Adding the repository root to ``sys.path`` has no user-visible effect and is
    what makes a script in a sub-directory able to import its own package, so it
    is not an import-time *side effect* in the sense this tool cares about.
    """
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in ("insert", "append", "extend")
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "path"
        and isinstance(func.value.value, ast.Name)
        # ``sys.path.append(...)`` and its aliased form ``_sys.path.append(...)``
        and func.value.value.id.lstrip("_") == "sys"
    )


def _pure_call(node: ast.Call) -> bool:
    if _is_path_bootstrap(node):
        return True
    func = node.func
    if isinstance(func, ast.Name):
        name = func.id
    elif isinstance(func, ast.Attribute):
        name = func.attr
    else:
        return False
    if name in PURE_CALLS:
        return True
    return False


def indent(chunk: str, first_line: int, width: int = 4) -> str:
    """Indent ``chunk`` by ``width`` spaces, leaving blank lines alone."""
    prefix = " " * width
    return "".join(
        (prefix + line) if line.strip() else line
        for line in chunk.splitlines(keepends=True)
    )


def _only_pure_calls(nodes: Sequence[ast.AST]) -> bool:
    calls = [n for node in nodes for n in ast.walk(node) if isinstance(n, ast.Call)]
    return bool(calls) and all(_pure_call(call) for call in calls)


def _raised_calls(nodes: Sequence[ast.AST]) -> set:
    """Ids of exception constructors that only build a ``raise`` operand."""
    found = set()
    for node in nodes:
        for child in ast.walk(node):
            if isinstance(child, ast.Raise) and child.exc is not None:
                found.add(id(child.exc))
    return found


def _has_call(nodes: Sequence[ast.AST], ignore: Sequence[str] = ()) -> bool:
    """True when one of ``nodes`` calls something that is not pure."""
    raised = _raised_calls(nodes)
    for node in nodes:
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            if id(child) in raised:
                continue
            if _pure_call(child):
                continue
            func = child.func
            if isinstance(func, ast.Name) and func.id in ignore:
                continue
            return True
    return False


def _is_effect(node: ast.stmt) -> bool:
    """True when the statement must not run at import time."""
    if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                         ast.AsyncFunctionDef, ast.ClassDef)):
        return False
    if _docstring(node):
        return False
    if _main_guard(node):
        return True
    if isinstance(node, (ast.Raise, ast.Assert, ast.Delete)):
        return True
    if isinstance(node, (ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)):
        # a loop/with block is only an effect when it calls something impure
        return _has_call(node.body)
    if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        value = getattr(node, "value", None)
        if value is None:
            return False
        if _only_pure_calls([value]):
            return False
        return _has_call([value])
    if isinstance(node, ast.If):
        return _has_call(node.body + node.orelse + [node.test])
    if isinstance(node, (ast.Expr, ast.Pass, ast.Global, ast.Nonlocal, ast.Match)):
        return not isinstance(node, ast.Pass) and not isinstance(node, (ast.Global, ast.Nonlocal))
    if isinstance(node, (ast.Try,)):
        return True
    return False


def _bound(statements: Sequence[ast.stmt]) -> set:
    names = set()
    for statement in statements:
        if isinstance(statement, ast.If) and _main_guard(statement):
            names |= _bound(statement.body)
            continue
        for node in ast.walk(statement):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    names |= _targets(target)
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
                names |= _targets(node.target)
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                names |= _targets(node.target)
            elif isinstance(node, ast.withitem) and node.optional_vars is not None:
                names |= _targets(node.optional_vars)
    return names


def _targets(node: ast.AST) -> set:
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.Tuple, ast.List)):
        names = set()
        for element in node.elts:
            names |= _targets(element)
    elif isinstance(node, ast.Starred):
        return _targets(node.value)
    else:
        return set()
    return names


# ---------------------------------------------------------------------------
# planning
# ---------------------------------------------------------------------------
def iter_python_files(root: str = REPO_ROOT):
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if name.endswith(".py"):
                yield os.path.join(base, name)


def third_party_imports(tree: ast.Module) -> List[str]:
    found = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            found.extend(a.name for a in node.names if a.name.split(".")[0] in THIRD_PARTY)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in THIRD_PARTY:
                found.append(node.module)
    return found


def plan(path: str) -> Optional[dict]:
    try:
        source = open(path, encoding="utf-8").read()
        tree = ast.parse(source)
    except (OSError, SyntaxError) as exc:
        return {"path": path, "kind": "unreadable", "detail": str(exc)}

    guarded = [node for node in tree.body if _main_guard(node)]
    effects = [
        i for i, node in enumerate(tree.body)
        if _is_effect(node) and not _main_guard(node)
    ]
    third = third_party_imports(tree)
    if not effects and not third:
        return None

    info = {
        "path": path,
        "kind": "guard-tail" if effects else "third-party",
        "effects": [tree.body[i].lineno for i in effects],
        "third_party": third,
        "globals": sorted(_bound([tree.body[i] for i in effects])),
        "already_guarded": bool(guarded),
    }
    return info


# ---------------------------------------------------------------------------
# transform
# ---------------------------------------------------------------------------
def transform(path: str, info: dict) -> str:
    """Return the rewritten source."""
    source = open(path, encoding="utf-8").read()
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)

    # Split the file into: file header + one chunk per top-level statement.
    # Leading comments/blank lines travel with the statement that follows them,
    # except before the first statement, where they are the file header
    # (shebang, banner comments) and must stay at the top.
    statements = list(tree.body)
    chunks: List[Tuple[int, str]] = []   # (first line number of the chunk, text)
    header_prefix = ""
    previous_end = 0
    for index, statement in enumerate(statements):
        start = getattr(statement, "lineno", previous_end + 1) - 1
        end = getattr(statement, "end_lineno", start + 1)
        trivia_start = previous_end
        trivia = "".join(lines[trivia_start:start])
        if index == 0:
            header_prefix = trivia
            trivia = ""
            trivia_start = start
        chunks.append((trivia_start + 1, trivia + "".join(lines[start:end])))
        previous_end = max(end, previous_end)

    trailing = "".join(lines[previous_end:])

    skip_indent = _string_continuation_lines(source)
    kept: List[str] = []
    moved: List[str] = []
    for statement, (chunk_line, chunk) in zip(statements, chunks):
        if _main_guard(statement):
            # merge the guard body into _main, dedented then re-indented
            guard_first = statement.body[0].lineno if statement.body else statement.lineno
            guard_body = _guard_body(statement, lines, skip_indent)
            moved.append(_indent(guard_body, guard_first, skip_indent))
        elif _is_effect(statement):
            moved.append(_indent(chunk, chunk_line, skip_indent))
        else:
            kept.append(chunk)

    header = (header_prefix + "".join(kept) + trailing).rstrip("\n")
    body_parts = []
    if info["globals"]:
        body_parts.append("    global " + ", ".join(info["globals"]) + "\n")
    body_parts.extend(moved)
    body = "".join(body_parts).rstrip("\n")
    if not body.strip():
        return source

    tail = "\n\n\n" + BANNER + "def _main():\n" + body + "\n\n\nif __name__ == \"__main__\":\n    _main()\n"
    result = header + tail
    compile(result, path, "exec")  # syntax check
    return result


def _string_continuation_lines(source: str) -> set:
    """Line numbers that are *inside* a multi-line string token.

    Those lines must never be re-indented, otherwise the string content the
    demo writes (HTML templates, JSON payloads) would change.
    """
    inside = set()
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type == tokenize.STRING and token.end[0] > token.start[0]:
                inside.update(range(token.start[0] + 1, token.end[0] + 1))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return set()
    return inside


def _indent(chunk: str, first_line: int, skip: set, prefix: str = "    ") -> str:
    """Indent a source chunk by ``prefix``, skipping multi-line string bodies."""
    out = []
    for offset, line in enumerate(chunk.splitlines(keepends=True)):
        lineno = first_line + offset
        if not line.strip() or lineno in skip:
            out.append(line)
        else:
            out.append(prefix + line)
    return "".join(out)


def _guard_body(node: ast.If, lines: List[str], skip: Optional[set] = None) -> str:
    """Return the body of an ``if __name__ == "__main__":`` block, dedented.

    Lines that belong to a multi-line string are never touched, otherwise the
    program text the demo writes would lose its own indentation.
    """
    if not node.body:
        return ""
    first = node.body[0].lineno - 1
    last = node.body[-1].end_lineno
    block = lines[first:last]
    protected = {number - 1 - first for number in (skip or set())}
    candidates = [
        len(line) - len(line.lstrip())
        for offset, line in enumerate(block)
        if line.strip() and offset not in protected
    ]
    trim = min(candidates) if candidates else 0
    out = []
    for offset, line in enumerate(block):
        if not line.strip() or offset in protected:
            out.append(line)
        else:
            out.append(line[trim:])
    return "".join(out)


# ---------------------------------------------------------------------------
# verification helpers
# ---------------------------------------------------------------------------
def normalise(text: str) -> str:
    for pattern, replacement in _VOLATILE:
        text = pattern.sub(replacement, text)
    return text


def run_script(path: str, timeout: int = 10) -> Tuple[int, str]:
    cwd = os.path.dirname(path) or REPO_ROOT
    env = dict(os.environ)
    env.setdefault("SUTRA_DATA_DIR", "/tmp/sutra-data")
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    try:
        completed = subprocess.run(
            [sys.executable, os.path.basename(path)],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return 124, ""
    return completed.returncode, completed.stdout.decode("utf-8", "replace")


def import_probe(path: str, timeout: int = 15) -> Tuple[bool, str]:
    code = (
        "import importlib.util, sys, os, io, contextlib\n"
        "p = %r\n"
        "sys.path.insert(0, os.path.dirname(os.path.abspath(p)))\n"
        "sys.path.insert(0, os.getcwd())\n"
        "spec = importlib.util.spec_from_file_location('probe_mod', p)\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "sys.modules['probe_mod'] = module\n"
        "with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):\n"
        "    spec.loader.exec_module(module)\n" % path
    )
    try:
        completed = subprocess.run(
            [sys.executable, "-c", code],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=os.path.dirname(path) or REPO_ROOT,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if completed.returncode == 0:
        return True, ""
    err = completed.stderr.decode("utf-8", "replace").strip().splitlines()
    return False, err[-1] if err else "unknown"


# ---------------------------------------------------------------------------
# cli
# ---------------------------------------------------------------------------
def hoist_pure_assignments(path: str) -> Optional[str]:
    """Move pure constant assignments out of ``_main``; return new source or None.

    Some modules keep an API constant inside their demo body, for example
    ``डिफ़ॉल्ट_मूल = os.path.expanduser(...)``.  Such an assignment has no side
    effect, so it belongs at module level; this repairs files that an older
    version of the transform moved behind the guard.
    """
    source = open(path, encoding="utf-8").read()
    tree = ast.parse(source)
    main = next(
        (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_main"),
        None,
    )
    if main is None:
        return None

    globals_decl = [n for n in main.body if isinstance(n, ast.Global)]
    allowed = set()
    for node in globals_decl:
        allowed.update(node.names)

    referenced = {
        n.id
        for node in tree.body
        if node is not main
        for n in ast.walk(node)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
    }

    hoist = []
    for statement in main.body:
        if not isinstance(statement, ast.Assign) or not isinstance(statement.value, ast.Call):
            continue
        if not _only_pure_calls([statement.value]):
            continue
        targets = {t.id for t in statement.targets if isinstance(t, ast.Name)}
        if not targets or not targets <= allowed:
            continue
        if not targets & referenced:
            continue
        hoist.append(statement)

    if not hoist:
        return None

    lines = source.splitlines(keepends=True)
    hoisted_text = "".join(
        "".join(lines[s.lineno - 1:s.end_lineno]) for s in hoist
    )
    hoisted_text = "\n".join(line[4:] if line.startswith("    ") else line
                             for line in hoisted_text.splitlines()) + "\n"

    remove_ranges = [(s.lineno - 1, s.end_lineno) for s in hoist]
    kept = []
    for index, line in enumerate(lines):
        if any(start <= index < end for start, end in remove_ranges):
            continue
        kept.append(line)
    result = "".join(kept)

    names = sorted({t.id for s in hoist for t in s.targets if isinstance(t, ast.Name)})
    for name in names:
        result = result.replace("    global " + name + "\n", "")
        result = result.replace(", " + name + "\n", "\n").replace("global " + name + ", ", "global ")

    marker = "# ---------------------------------------------------------------------------\n# Demo body."
    if marker in result:
        result = result.replace(marker, hoisted_text + "\n\n" + marker, 1)
    else:
        result += "\n" + hoisted_text

    # ``_main`` must keep a non-empty body after the hoist.
    try:
        compile(result, path, "exec")
    except IndentationError:
        result = result.replace(
            "def _main():\n", "def _main():\n    pass\n", 1
        )
        compile(result, path, "exec")
    return result


MAIN_TAIL = (
    'if __name__ == "__main__":\n'
    '    try:\n'
    '        from brahma_cli import चलाओ as _brahma_cli_run\n'
    '    except ImportError:  # script copied outside the repository\n'
    '        _main()\n'
    '    else:\n'
    '        raise SystemExit(_brahma_cli_run(_main))\n'
)


def wrap_main_tail(path: str) -> Optional[str]:
    """Route the ``__main__`` block through :func:`brahma_cli.चलाओ`.

    Turns an ``EOFError`` traceback (stdin closed) into exit code 2 with a clear
    message, and Ctrl-C into 130 — while leaving genuine errors visible.
    """
    source = open(path, encoding="utf-8").read()
    if "_brahma_cli_run" in source or "from brahma_cli import" in source:
        return None

    marker = 'if __name__ == "__main__":'
    index = source.rfind(marker)
    if index == -1:
        return None
    tail = source[index:]
    if "_main()" not in tail:
        return None
    rest = tail[len(marker):].strip()
    if rest not in ("_main()", "raise SystemExit(_main())", "_main()\n"):
        return None

    result = source[:index].rstrip("\n") + "\n\n\n" + MAIN_TAIL
    compile(result, path, "exec")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="rewrite files")
    parser.add_argument("--json", help="write the plan as JSON")
    parser.add_argument("--only", help="restrict to paths containing this substring")
    parser.add_argument("--files-from", help="apply only to the paths listed in this file")
    parser.add_argument("--hoist-pure", action="store_true",
                        help="move pure constants out of _main (repair mode)")
    parser.add_argument("--wrap-main", action="store_true",
                        help="route __main__ through brahma_cli.चलाओ")
    args = parser.parse_args(argv)

    if args.wrap_main:
        wrapped = 0
        for path in iter_python_files():
            if args.only and args.only not in path:
                continue
            try:
                new_source = wrap_main_tail(path)
            except (OSError, SyntaxError) as exc:
                print("SKIP    %s (%s)" % (os.path.relpath(path, REPO_ROOT), exc))
                continue
            if new_source:
                open(path, "w", encoding="utf-8").write(new_source)
                wrapped += 1
        print("%d files routed through brahma_cli.चलाओ" % wrapped)
        return 0

    if args.hoist_pure:
        repaired = 0
        for path in iter_python_files():
            if args.only and args.only not in path:
                continue
            try:
                new_source = hoist_pure_assignments(path)
            except (OSError, SyntaxError) as exc:
                print("SKIP    %s (%s)" % (os.path.relpath(path, REPO_ROOT), exc))
                continue
            if new_source:
                open(path, "w", encoding="utf-8").write(new_source)
                print("HOIST   %s" % os.path.relpath(path, REPO_ROOT))
                repaired += 1
        print("\n%d files repaired" % repaired)
        return 0

    wanted = None
    if args.files_from:
        with open(args.files_from, encoding="utf-8") as handle:
            wanted = {line.strip() for line in handle if line.strip()}

    plans = []
    for path in iter_python_files():
        if wanted is not None and os.path.relpath(path, REPO_ROOT) not in wanted:
            continue
        if args.only and args.only not in path:
            continue
        info = plan(path)
        if info:
            plans.append(info)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(plans, handle, ensure_ascii=False, indent=2)

    if not args.apply:
        for info in plans:
            print("%-9s %s" % (info["kind"], os.path.relpath(info["path"], REPO_ROOT)))
        print("\n%d files with import-time side effects" % len(plans))
        return 0

    changed = skipped = 0
    for info in plans:
        path = info["path"]
        rel = os.path.relpath(path, REPO_ROOT)
        original = open(path, encoding="utf-8").read()
        if info["kind"] != "guard-tail":
            print("MANUAL  %s (third-party import: %s)" % (rel, ", ".join(info["third_party"])))
            skipped += 1
            continue

        before = run_script(path)
        try:
            new_source = transform(path, info)
        except Exception as exc:  # noqa: BLE001 - report and skip
            print("SKIP    %s (%s)" % (rel, exc))
            skipped += 1
            continue

        with open(path, "w", encoding="utf-8") as handle:
            handle.write(new_source)

        after = run_script(path)
        same = (after[0], normalise(after[1])) == (before[0], normalise(before[1]))
        ok, reason = import_probe(path)

        if not same or not ok:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(original)
            why = "behaviour changed" if not same else "import failed: %s" % reason[:70]
            print("REVERT  %-58s %s" % (rel[:58], why))
            skipped += 1
            continue

        print("OK      %s" % rel)
        changed += 1

    print("\n%d files rewritten and verified, %d skipped" % (changed, skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
