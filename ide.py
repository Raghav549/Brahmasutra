"""सूत्र IDE — a small menu-driven launcher.

Every command used to be ``os.system(f"चलाओ {file}")``: the file name was
pasted into a shell string, so a name like ``x; rm -rf ~`` would have been
executed.  Commands are now run as argument vectors with
:mod:`subprocess`, and only the built-in actions are offered.

>>> menu_items()[0]
'1. file चलाओ'
"""

from __future__ import annotations

import shutil
import subprocess
import sys

#: command → what to run (argument vector).  ``{file}`` is substituted as a
#: *single* argument, never through a shell.
COMMANDS = {
    "चलाओ": [sys.executable, "-m", "brahma", "run"],
    "संस्कृत-compile": [sys.executable, "-m", "brahma", "compile"],
}


def शीर्षक():
    print("===================================")
    print("        सूत्र IDE")
    print("===================================")


def menu_items():
    return [
        "1. file चलाओ",
        "2. compile",
        "3. APK निर्माण",
        "4. version",
        "5. exit",
    ]


def मेनू():
    print("")
    for item in menu_items():
        print(item)
    print("")


def _run(argv, label):
    """Run ``argv`` without a shell; report a missing executable honestly."""
    if shutil.which(argv[0]) is None and not argv[0].endswith("python"):
        print("आदेश उपलब्ध नहीं:", label)
        return 2
    try:
        return subprocess.run(argv, check=False).returncode
    except OSError as exc:
        print("आदेश विफल:", label, "—", exc)
        return 1


def चलाओ(path):
    """Run a सूत्र file through the engine."""
    return _run(COMMANDS["चलाओ"] + [path], "चलाओ")


def compile(path):  # noqa: A001 - mirrors the menu wording
    """Compile a सूत्र file through the engine."""
    return _run(COMMANDS["संस्कृत-compile"] + [path], "compile")


def निर्माण(path):
    """Build a ZIP bundle for ``path``."""
    from brahma_packaging import build_bundle
    import os

    output = os.path.dirname(os.path.abspath(path)) or "."
    return build_bundle(os.path.splitext(os.path.basename(path))[0], [path], output).path


def version():
    import brahma

    print("BRAHMA", brahma.__version__)
    return 0


def main(argv=None):
    """Interactive menu (falls back to a message when stdin is closed)."""
    शीर्षक()
    मेनू()
    try:
        choice = input("विकल्प: ").strip()
    except EOFError:
        print("इंटरैक्टिव टर्मिनल आवश्यक है।")
        return 2

    if choice == "5":
        return 0
    if choice == "4":
        return version()
    if choice in ("1", "2", "3"):
        try:
            path = input("file नाम: ").strip()
        except EOFError:
            print("file नाम आवश्यक है।")
            return 2
        return {"1": चलाओ, "2": compile, "3": निर्माण}[choice](path)
    print("अज्ञात विकल्प")
    return 2


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
