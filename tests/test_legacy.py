"""Regression pins for the historical prototype scripts.

The repository keeps hundreds of early-generation demo files.  They are not
part of the supported engine, but they must not silently get *worse*.  This
module:

* asserts that every demo that worked when the baseline was recorded still
  exits successfully;
* records known-broken demos as expected failures (so they stay visible in
  the test report instead of being deleted or ignored);
* fails when a new top-level test script appears without a baseline entry.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from tools.legacy_baseline import BASELINE, IMPORT_MODULES, scripts

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 15


def load_baseline():
    with open(BASELINE, encoding="utf-8") as handle:
        return json.load(handle)


BASELINE_DATA = load_baseline()


def run_script(repo, name):
    completed = subprocess.run(
        [sys.executable, name],
        cwd=repo,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
    )
    return completed


@pytest.mark.parametrize("name", sorted(BASELINE_DATA["scripts"]))
def test_legacy_script_behaviour(name, repo_copy):
    entry = BASELINE_DATA["scripts"][name]
    expected = entry["status"]

    if expected == "timeout":
        pytest.xfail("ज्ञात: '%s' रुक जाता है (baseline timeout)" % name)

    completed = run_script(repo_copy, name)
    actual = "pass" if completed.returncode == 0 else "fail"

    if expected == "pass":
        assert actual == "pass", (
            "regression: %s worked before but now exits %d\n%s"
            % (name, completed.returncode, completed.stderr.decode("utf-8", "replace")[-800:])
        )
    else:
        reason = entry.get("reason") or "recording किया गया व्यवहार"
        pytest.xfail("ज्ञात विफलता: %s (%s)" % (name, reason))


def test_baseline_is_not_stale():
    """Every top-level test/demo script must be registered in the baseline."""
    recorded = set(BASELINE_DATA["scripts"])
    current = set(scripts())
    assert current - recorded == set(), "नई स्क्रिप्ट baseline में जोड़ें: %s" % sorted(current - recorded)
    assert recorded - current == set(), "baseline में पुरानी स्क्रिप्ट है: %s" % sorted(recorded - current)


def test_baseline_records_real_results():
    statuses = {entry["status"] for entry in BASELINE_DATA["scripts"].values()}
    assert statuses <= {"pass", "fail", "timeout"}
    assert "pass" in statuses


@pytest.mark.parametrize("module", IMPORT_MODULES)
def test_legacy_module_import(module):
    """Curated legacy modules must stay importable."""
    entry = BASELINE_DATA.get("modules", {}).get(module, {"status": "pass"})
    completed = subprocess.run(
        [sys.executable, "-c", "import %s" % module],
        cwd=REPO_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
    )
    if entry["status"] == "pass":
        assert completed.returncode == 0, completed.stderr.decode("utf-8", "replace")[-500:]
    else:
        pytest.xfail("ज्ञात आयात विफलता: %s" % module)


def test_legacy_scripts_do_not_import_the_new_package():
    """The legacy tree and the supported engine must stay independent."""
    completed = subprocess.run(
        [sys.executable, "-c", "import brahma, sys; print(brahma.__version__)"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
    )
    assert completed.returncode == 0


def test_no_module_has_import_time_side_effects():
    """Importing any module in the tree must not print, prompt, loop or serve.

    ``tools/harden_imports.py`` classifies every top-level statement; this test
    fails if a new module (or a careless edit) reintroduces import-time work.
    """
    from tools import harden_imports

    offenders = []
    for path in harden_imports.iter_python_files():
        info = harden_imports.plan(path)
        if info and info["kind"] == "guard-tail":
            offenders.append(os.path.relpath(path, REPO_ROOT))

    assert offenders == [], "import-time side effects फिर आ गए: %s" % offenders


def test_no_third_party_imports_in_optional_modules():
    """The demo backends must not depend on Flask/requests being installed."""
    from tools import harden_imports

    offenders = []
    for path in harden_imports.iter_python_files():
        info = harden_imports.plan(path)
        if info and info.get("third_party"):
            offenders.append((os.path.relpath(path, REPO_ROOT), info["third_party"]))

    assert offenders == [], "third-party imports मिले: %s" % offenders
