"""🕉️ सूत्र-OS — the project's own kernel image, built and booted here.

The repository always claimed to have "its own kernel".  It now does, in a way
that can be executed and verified:

* the kernel is a **सूत्र program** (:data:`KERNEL_SOURCE`), not a `.py` file
  pretending to be an OS;
* it is compiled by ``brahma.compiler`` to the project's own bytecode;
* it is packed into the project's own boot image format
  (``b"SUTRAOS" + version + length + bytecode`` — the same signature
  ``brahma_bytecode.IMAGE_SIGNATURE`` already used in the tree);
* :func:`verify` boots the image on ``brahma.vm`` and requires the boot banner,
  a passing self-test and the ``READY`` line, so a broken image cannot be
  installed;
* the LLM may rewrite the kernel source (``brahma llm evolve --os``) — but only
    a build that boots and self-tests cleanly replaces the installed image.

Boot flow of the shipped kernel: banner → register/arithmetic self-test →
bytecode sanity check → ``READY``.
"""

from __future__ import annotations

import os
import struct
from typing import Dict, List, Optional, Tuple

from brahma.bytecode import dump_bytecode, load_bytecode
from brahma.bytecode import IMAGE_SIGNATURE, IMAGE_VERSION
from brahma.compiler import compile_source
from brahma.vm import VM

#: The OS itself.  Deliberately small, complete and executable.
KERNEL_SOURCE = r'''
# 🕉️ सूत्र-OS कर्नेल — यह प्रोग्राम ही ऑपरेटिंग सिस्टम है।
दर्शय "🕉️ सूत्र-OS कर्नेल प्रारम्भ"

कार्य परीक्षण(नाम, मान)
    यदि मान == सत्य
        प्रत्यागमन "ठीक"
    अन्त
    प्रत्यागमन "विफल"
अन्त

कार्य योग(a, b)
    प्रत्यागमन a + b
अन्त

कार्य गुणन(a, b)
    प्रत्यागमन a * b
अन्त

# --- स्व-परीक्षण -------------------------------------------------------
स्थापय अ = योग(2, 3)
स्थापय ब = गुणन(4, 5)
स्थापय जाँच1 = अ == 5
स्थापय जाँच2 = ब == 20
दर्शय "स्व-परीक्षण: " + परीक्षण("योग", जाँच1) + " / " + परीक्षण("गुणन", जाँच2)

# --- स्मृति ------------------------------------------------------------
स्थापय स्मृति = [सत्य, 1, 2, 3]
स्थापय i = 0
यावत् i < 3
    जोड़ें(स्मृति, अ + ब + i)
    i = i + 1
अन्त
दर्शय "स्मृति इकाइयाँ: " + पाठ(लम्बाई(स्मृति))

यदि जाँच1 च जाँच2
    दर्शय "READY"
अन्त
'''

KERNEL_NAME = "सूत्र-OS"


def build_image(source: Optional[str] = None, version: int = IMAGE_VERSION) -> bytes:
    """Compile ``source`` (default :data:`KERNEL_SOURCE`) into a boot image."""
    code = compile_source(source if source is not None else KERNEL_SOURCE,
                          source_name="<sutra-os>")
    payload = dump_bytecode(code)
    return b"".join([
        IMAGE_SIGNATURE,
        struct.pack(">I", version),
        struct.pack(">I", len(payload)),
        payload,
    ])


def unpack_image(image: bytes) -> Tuple[int, bytes]:
    """Split a boot image into ``(version, bytecode_blob)``."""
    if not image.startswith(IMAGE_SIGNATURE):
        raise ValueError("अमान्य boot image: signature नहीं मिला")
    head = len(IMAGE_SIGNATURE)
    if len(image) < head + 8:
        raise ValueError("अधूरा boot image header")
    version, size = struct.unpack(">II", image[head:head + 8])
    blob = image[head + 8:head + 8 + size]
    if len(blob) != size:
        raise ValueError("अधूरा boot image: %d बाइट चाहिए, मिले %d" % (size, len(blob)))
    return version, blob


def boot(image: Optional[bytes] = None, step_limit: int = 200_000) -> Dict[str, object]:
    """Boot an image (default: the shipped kernel) and return the boot log."""
    image = build_image() if image is None else image
    version, blob = unpack_image(image)
    code = load_bytecode(blob)
    lines: List[str] = []
    vm = VM(out=lines.append, step_limit=step_limit)
    value = vm.run(code)
    return {
        "version": version,
        "name": KERNEL_NAME,
        "output": lines,
        "steps": vm.steps,
        "value": value,
        "ready": "READY" in lines,
        "image_bytes": len(image),
    }


def verify(image: Optional[bytes] = None) -> Dict[str, object]:
    """Boot and assert the banner + self-test + READY contract."""
    report = boot(image)
    problems = []
    if not report["output"]:
        problems.append("कर्नेल ने कुछ नहीं छापा")
    else:
        if "सूत्र-OS" not in report["output"][0]:
            problems.append("boot banner अनुपस्थित")
        if not any("स्व-परीक्षण: ठीक / ठीक" in line for line in report["output"]):
            problems.append("स्व-परीक्षण विफल")
        if not report["ready"]:
            problems.append("READY पंक्ति अनुपस्थित")
    report["ok"] = not problems
    report["problems"] = problems
    return report


def image_path() -> str:
    """Where the installed image lives (``$BRAHMA_HOME/os/sutra-os.img``)."""
    from brahma_paths import data_root

    return os.path.join(data_root("os", create=True), "sutra-os.img")


def install(image: Optional[bytes] = None, path: Optional[str] = None) -> str:
    """Verify, then atomically write the image; return its path."""
    image = build_image() if image is None else image
    report = verify(image)
    if not report["ok"]:
        raise RuntimeError("कर्नेल सत्यापन विफल: %s" % ", ".join(report["problems"]))
    target = path or image_path()
    temporary = target + ".tmp"
    with open(temporary, "wb") as handle:
        handle.write(image)
    os.replace(temporary, target)
    return target


def read_image(path: Optional[str] = None) -> bytes:
    with open(path or image_path(), "rb") as handle:
        return handle.read()


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="सूत्र-OS कर्नेल")
    parser.add_argument("action", nargs="?", default="verify",
                        choices=("build", "boot", "verify", "install", "info"))
    parser.add_argument("--out", default=None, help="image फ़ाइल")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.action == "build":
        target = args.out or image_path()
        with open(target, "wb") as handle:
            handle.write(build_image())
        print("🕉️ image निर्मित: %s" % target)
        return 0
    if args.action == "install":
        print("🕉️ स्थापित: %s" % install(path=args.out))
        return 0
    if args.action == "info":
        image = build_image()
        version, blob = unpack_image(image)
        print("🕉️ %s\n  संस्करण: %d\n  आकार: %d बाइट" % (KERNEL_NAME, version, len(image)))
        return 0

    report = verify() if args.action == "verify" else boot()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    else:
        for line in report["output"]:
            print(line)
        print("  चरण: %d, छवि: %d बाइट, स्थिति: %s"
              % (report["steps"], report["image_bytes"], "ठीक" if report.get("ok", True) else "विफल"))
    return 0 if report.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
