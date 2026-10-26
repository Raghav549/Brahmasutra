"""🕉️ सूत्र Bootable Image Builder — builds the real ``SUTRAOS`` image.

The old version wrote a 10-byte header plus whatever ``परीक्षण.सूत्रबिन``
happened to be lying around, so the "bootable image" could never boot.  It now
delegates to :mod:`brahma_llm.kernel`, which compiles an actual सूत्र kernel to
bytecode, packs the documented image format and verifies the boot contract
before writing anything to disk.

    python सूत्र_boot_image_builder.py            # build + verify → data dir
    python सूत्र_boot_image_builder.py --boot     # build, verify, boot
"""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

IMAGE_NAME = "सूत्र.img"


def build(path: str = None) -> str:
    """Build and verify the image; return the path it was written to."""
    from brahma_llm.kernel import build_image, install, verify

    image = build_image()
    report = verify(image)
    if not report["ok"]:
        raise RuntimeError("image सत्यापन विफल: %s" % ", ".join(report["problems"]))
    target = path or install()
    if path:
        with open(path, "wb") as handle:
            handle.write(image)
    print("🕉️ SUTRAOS image निर्मित: %s (%d बाइट)" % (target, len(image)))
    return target


def boot(path: str = None) -> int:
    """Boot the built image and print the boot log."""
    from brahma_llm.kernel import boot as boot_image

    report = boot_image()
    for line in report["output"]:
        print(line)
    return 0 if report["ready"] else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="सूत्र bootable image")
    parser.add_argument("--out", default=None, help="image फ़ाइल (डिफ़ॉल्ट: डेटा निर्देशिका)")
    parser.add_argument("--boot", action="store_true", help="बनाने के बाद बूट करें")
    args = parser.parse_args(argv)

    path = build(args.out)
    if args.boot:
        return boot(path)
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        raise SystemExit(main())
    else:
        raise SystemExit(_brahma_cli_run(main))
