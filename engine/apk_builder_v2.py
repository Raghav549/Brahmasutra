"""Android bundle builder (v2) — honest replacement.

This module used to write a three-line text file named ``<app>.apk`` and print
"APK सफलतया निर्मित".  It now builds a real ZIP bundle through
:mod:`brahma_packaging`; :func:`brahma_packaging.is_installable_apk` reports it
as not installable, which is the truth.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)


import os

from brahma_packaging import build_bundle

OUTPUT_DIR = os.environ.get("BRAHMA_APK_OUTPUT") or os.path.expanduser("~/सूत्र-तंत्र/apk_output")


def निर्माण(file, output_dir=None):
    """Bundle ``file`` (or the sources next to it) into a ZIP; return its path."""
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    name = os.path.splitext(os.path.basename(file))[0]
    output_dir = output_dir or OUTPUT_DIR
    sources = [file]

    # bundle the whole project directory when the file lives in one
    parent = os.path.dirname(os.path.abspath(file))
    if os.path.basename(parent) in ("backend", "frontend", "app", "src"):
        sources = [os.path.dirname(parent)]

    bundle = build_bundle(name, sources, output_dir, flavour=2)
    print("ZIP बंडल निर्मित (स्थापन योग्य APK नहीं):")
    print(bundle.summary())
    return bundle.path


def स्थापित(apk, destination=None):
    """Copy the bundle to a destination directory; raise if it is missing."""
    import shutil

    if not os.path.exists(apk):
        raise FileNotFoundError(apk)
    destination = destination or os.path.expanduser("~/Downloads")
    os.makedirs(destination, exist_ok=True)
    target = os.path.join(destination, os.path.basename(apk))
    shutil.copy(apk, target)
    print("बंडल कॉपी किया गया:", target)
    return target


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Android ZIP bundle (v2)")
    parser.add_argument("file")
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)
    निर्माण(args.file, args.output)
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
