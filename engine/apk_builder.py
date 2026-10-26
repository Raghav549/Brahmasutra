"""Android bundle builder (v1) — produces a ZIP bundle, not an APK.

Historically this function zipped the project with a fake ``classes.dex``
(``b"SUTRA_DEX_PLACEHOLDER"``) and printed *"Installable APK निर्मित"*.  It now
delegates to :mod:`brahma_packaging` and states plainly what it produced.

>>> apk_निर्माण("demo", sources=[], output_dir="/tmp/x")  # doctest: +SKIP
"""

from __future__ import annotations

import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)


import os

from brahma_packaging import build_bundle

BASE = os.environ.get("BRAHMA_HOME") or os.path.expanduser("~/सूत्र-तंत्र")


def apk_निर्माण(app_name, sources=None, output_dir=None):
    """Zip ``sources`` into ``output_dir``; return a :class:`Bundle`."""
    output_dir = output_dir or os.path.join(BASE, "output")
    if sources is None:
        sources = [
            os.path.join(BASE, "android_projects", app_name),
        ]
    existing = [path for path in sources if os.path.exists(path)]
    if not existing:
        raise FileNotFoundError(
            "कोई स्रोत नहीं मिला: %s (पहले android_structure.py से परियोजना बनाएँ)"
            % ", ".join(sources)
        )

    bundle = build_bundle(app_name, existing, output_dir, flavour=1)
    print("ZIP बंडल निर्मित (APK नहीं — हस्ताक्षर/aapt2 आवश्यक):")
    print(bundle.summary())
    return bundle


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Android ZIP bundle बनाएँ")
    parser.add_argument("app")
    parser.add_argument("--sources", nargs="*", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)
    apk_निर्माण(args.app, args.sources, args.output)
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
