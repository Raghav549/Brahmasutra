"""Android bundle engine — a thin wrapper over :mod:`brahma_packaging`.

The old version wrote a plain-XML manifest and ``b"sutra-dex"`` as
``classes.dex``, then printed "APK सफलतापूर्वक निर्मित".  That file is a ZIP
archive, not an APK, and the text now says so.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)


import os

from brahma_packaging import build_bundle, describe

BASE = os.environ.get("BRAHMA_HOME") or os.path.expanduser("~/सूत्र-तंत्र")


def apk_निर्माण(project_name, sources=None, output_dir=None):
    """Create a ZIP bundle for ``project_name``; return its path."""
    output_dir = output_dir or os.path.join(BASE, "apk_output")
    sources = sources or [os.path.join(BASE, "apk_build", project_name)]
    existing = [path for path in sources if os.path.exists(path)]
    if not existing:
        raise FileNotFoundError(
            "परियोजना नहीं मिली: %s" % (sources,)
        )
    bundle = build_bundle(project_name, existing, output_dir, flavour=3)
    print("बंडल निर्मित:", bundle.summary())
    print("जाँच:", describe(bundle.path))
    return bundle.path


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Android ZIP bundle इंजन")
    parser.add_argument("project")
    args = parser.parse_args(argv)
    apk_निर्माण(args.project)
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
