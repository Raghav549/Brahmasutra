"""🕉️ सूत्र bytecode — one documented format for every compiler in the repo.

Before this module the repository contained five "compilers" that wrote *four
incompatible* encodings (4-byte opcodes, ``struct`` records, text lines…), so a
``.यन्त्र`` file produced by one of them could not be executed by any of the
machines.  Everything now assembles to:

======  =========================  ========================================
opcode  mnemonic                   operands
======  =========================  ========================================
1       ``संकल्प`` / ``स्थापय``    ``reg`` (1 byte), ``value`` (4 bytes BE)
2       ``योग``                    ``reg1``, ``reg2``
3       ``घटा``                    ``reg1``, ``reg2``
4       ``गुण``                    ``reg1``, ``reg2``
5       ``दर्शय``                  ``reg``
6       ``निर्गम``                 —
======  =========================  ========================================

Registers are single letters: ``अ``=1, ``ब``=2, ``स``=3, ``द``=4.

>>> program = assemble("संकल्प अ 50\\nसंकल्प ब 70\\nयोग अ ब\\nदर्शय अ")
>>> run(program)["अ"]
दर्शय: अ = 120
120
"""

from __future__ import annotations

import struct

from brahma.bytecode import IMAGE_SIGNATURE as _IMAGE_SIGNATURE  # noqa: F401
from brahma import bytecode as _canonical_image
from typing import Dict, Iterable, Optional

__all__ = [
    "assemble",
    "assemble_file",
    "run",
    "disassemble",
    "pack_image",
    "unpack_image",
    "Machine",
    "असेंबली_त्रुटि",
    "OPCODES",
    "REGISTERS",
    "IMAGE_SIGNATURE",
]

OPCODES = {"संकल्प": 1, "स्थापय": 1, "योग": 2, "घटा": 3, "गुण": 4, "दर्शय": 5, "निर्गम": 6}
REGISTERS = {"अ": 1, "ब": 2, "स": 3, "द": 4}
NAMES = {value: name for name, value in REGISTERS.items()}
NAMES = {**NAMES, 0: "?"}
HALT = 6


class असेंबली_त्रुटि(Exception):
    """Raised for an unknown mnemonic, register or malformed bytecode."""


def _register(name: str) -> int:
    if name not in REGISTERS:
        raise असेंबली_त्रुटि(
            "अज्ञात रजिस्टर %r (समर्थित: %s)" % (name, ", ".join(sorted(REGISTERS)))
        )
    return REGISTERS[name]


def assemble(text: str) -> bytes:
    """Assemble सूत्र source text into bytecode.

    Raises :class:`असेंबली_त्रुटि` for anything it does not understand, instead
    of silently emitting a bogus opcode.
    """
    out = bytearray()
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        mnemonic = parts[0]
        if mnemonic not in OPCODES:
            raise असेंबली_त्रुटि("पंक्ति %d: अज्ञात आदेश %r" % (number, mnemonic))
        opcode = OPCODES[mnemonic]

        if opcode == 1:
            if len(parts) != 3:
                raise असेंबली_त्रुटि("पंक्ति %d: %s का रूप 'reg मान' है" % (number, mnemonic))
            value = int(parts[2])
            if not -2 ** 31 <= value < 2 ** 31:
                raise असेंबली_त्रुटि("पंक्ति %d: मान 32-बिट सीमा से बाहर" % number)
            out += struct.pack(">BBI", opcode, _register(parts[1]), value & 0xFFFFFFFF)
        elif opcode in (2, 3, 4):
            if len(parts) != 3:
                raise असेंबली_त्रुटि("पंक्ति %d: %s का रूप 'reg reg' है" % (number, mnemonic))
            out += struct.pack(">BBB", opcode, _register(parts[1]), _register(parts[2]))
        elif opcode == 5:
            if len(parts) != 2:
                raise असेंबली_त्रुटि("पंक्ति %d: दर्शय का रूप 'reg' है" % number)
            out += struct.pack(">BB", opcode, _register(parts[1]))
        else:
            out.append(HALT)
    if HALT not in out:
        out.append(HALT)
    return bytes(out)


def assemble_file(source: str, target: str) -> bytes:
    """Assemble ``source`` into ``target``; return the bytecode."""
    with open(source, "r", encoding="utf-8") as handle:
        code = assemble(handle.read())
    with open(target, "wb") as handle:
        handle.write(code)
    return code


def disassemble(code: bytes) -> str:
    """Return a readable listing of ``code`` (useful in tests)."""
    index = 0
    lines = []
    while index < len(code):
        opcode = code[index]
        index += 1
        if opcode == 1:
            if index + 5 > len(code):
                raise असेंबली_त्रुटि("अपूर्ण SET")
            register = code[index]
            value = struct.unpack(">i", code[index + 1:index + 5])[0]
            index += 5
            lines.append("संकल्प %s %d" % (NAMES.get(register, register), value))
        elif opcode in (2, 3, 4):
            if index + 2 > len(code):
                raise असेंबली_त्रुटि("अपूर्ण arithmetic")
            first, second = code[index], code[index + 1]
            index += 2
            name = {2: "योग", 3: "घटा", 4: "गुण"}[opcode]
            lines.append("%s %s %s" % (name, NAMES.get(first, first), NAMES.get(second, second)))
        elif opcode == 5:
            register = code[index]
            index += 1
            lines.append("दर्शय %s" % NAMES.get(register, register))
        elif opcode == HALT:
            lines.append("निर्गम")
            break
        else:
            raise असेंबली_त्रुटि("अज्ञात ऑपकोड %d" % opcode)
    return "\n".join(lines)


class Machine:
    """A bytecode interpreter with 이름이 있는 registers."""

    def __init__(self, verbose: bool = True) -> None:
        self.registers: Dict[str, int] = {}
        self.verbose = verbose

    def run(self, code: bytes) -> Dict[str, int]:
        """Execute ``code`` and return the final register state."""
        index = 0
        length = len(code)
        while index < length:
            opcode = code[index]
            index += 1

            if opcode == 1:
                if index + 5 > length:
                    raise असेंबली_त्रुटि("अपूर्ण SET निर्देश")
                register = NAMES.get(code[index], "?")
                value = struct.unpack(">i", code[index + 1:index + 5])[0]
                index += 5
                self.registers[register] = value
                self._say("स्थापित: %s = %d" % (register, value))
            elif opcode in (2, 3, 4):
                if index + 2 > length:
                    raise असेंबली_त्रुटि("अपूर्ण निर्देश")
                first = NAMES.get(code[index], "?")
                second = NAMES.get(code[index + 1], "?")
                index += 2
                if first not in self.registers or second not in self.registers:
                    raise असेंबली_त्रुटि("अज्ञात रजिस्टर: %s/%s" % (first, second))
                if opcode == 2:
                    self.registers[first] += self.registers[second]
                    label = "योग"
                elif opcode == 3:
                    self.registers[first] -= self.registers[second]
                    label = "घटा"
                else:
                    self.registers[first] *= self.registers[second]
                    label = "गुण"
                self._say("%s: %s = %d" % (label, first, self.registers[first]))
            elif opcode == 5:
                if index >= length:
                    raise असेंबली_त्रुटि("अपूर्ण दर्शय")
                register = NAMES.get(code[index], "?")
                index += 1
                if register not in self.registers:
                    raise असेंबली_त्रुटि("अज्ञात रजिस्टर: %s" % register)
                self._say("दर्शय: %s = %d" % (register, self.registers[register]))
            elif opcode == HALT:
                break
            else:
                raise असेंबली_त्रुटि("अज्ञात ऑपकोड %d" % opcode)

        return dict(self.registers)

    def _say(self, message: str) -> None:
        if self.verbose:
            print(message)


def run(code: bytes, verbose: bool = True) -> Dict[str, int]:
    """Execute ``code`` in a fresh machine and return its registers."""
    return Machine(verbose=verbose).run(code)


# The image format is defined once, in ``brahma.bytecode``; these names are
# re-exported so existing callers keep working without a second definition.
IMAGE_SIGNATURE = _canonical_image.IMAGE_SIGNATURE
IMAGE_VERSION = _canonical_image.IMAGE_VERSION


def pack_image(kernel: bytes, version: int = IMAGE_VERSION) -> bytes:
    """Wrap bytecode in a boot image: signature + version + size + kernel."""
    if not isinstance(kernel, (bytes, bytearray)):
        raise असेंबली_त्रुटि("kernel बाइट्स होना चाहिए")
    return b"".join(
        [
            IMAGE_SIGNATURE,
            struct.pack(">I", version),
            struct.pack(">I", len(kernel)),
            bytes(kernel),
        ]
    )


def unpack_image(image: bytes):
    """Split a boot image into ``(version, kernel)``.

    >>> unpack_image(pack_image(b"\\x06"))
    (1, b'\\x06')
    """
    if not isinstance(image, (bytes, bytearray)):
        raise असेंबली_त्रुटि("image बाइट्स होना चाहिए")
    if not image.startswith(IMAGE_SIGNATURE):
        raise असेंबली_त्रुटि("अमान्य image signature")
    header = len(IMAGE_SIGNATURE)
    if len(image) < header + 8:
        raise असेंबली_त्रुटि("अपूर्ण image header")
    version, size = struct.unpack(">II", image[header:header + 8])
    kernel = bytes(image[header + 8:header + 8 + size])
    if len(kernel) != size:
        raise असेंबली_त्रुटि(
            "image अपूर्ण: %d बाइट चाहिए, मिले %d" % (size, len(kernel))
        )
    return version, kernel
