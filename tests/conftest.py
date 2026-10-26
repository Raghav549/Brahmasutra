"""Shared test helpers."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from brahma import execute  # noqa: E402  (path setup must happen first)


def run(source, **kwargs):
    """Compile and run BRAHMA source; return the ExecutionResult."""
    return execute(source, **kwargs)


def output_of(source, **kwargs):
    """Run source and return its captured output lines (asserts no error)."""
    result = execute(source, **kwargs)
    assert result.ok, "unexpected error: %s" % (result.error.format() if result.error else "")
    return result.output


def python_exec(code):
    """Run Python code in a subprocess and return (returncode, stdout, stderr)."""
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    return (
        completed.returncode,
        completed.stdout.decode("utf-8", "replace"),
        completed.stderr.decode("utf-8", "replace"),
    )


@pytest.fixture(scope="session")
def repo_copy(tmp_path_factory):
    """A throw-away copy of the repository used to run legacy scripts safely.

    Legacy demos write files into the working directory; running them in a
    copy keeps the checkout clean and makes the tests repeatable.
    """
    target = tmp_path_factory.mktemp("brahma_repo") / "repo"
    shutil.copytree(
        REPO_ROOT,
        str(target),
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "*.pyc"),
        symlinks=True,
    )
    return str(target)
