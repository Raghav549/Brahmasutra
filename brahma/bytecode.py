"""Bytecode representation, validation and (de)serialisation.

A BRAHMA bytecode image is a UTF-8 JSON document::

    {
      "format": "brahma-bytecode",
      "version": 1,
      "entry": { ... CodeObject ... }
    }

Using a documented, human-diffable container (rather than ad-hoc binary
bytes) makes compiled programs portable across Python versions and lets
``python -m brahma disasm`` show exactly what will run.
"""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .errors import BytecodeError

FORMAT_NAME = "brahma-bytecode"
FORMAT_VERSION = 1
MAGIC = b"SUTRA1\n"

#: Every instruction the VM understands.  Keeping the table in one place
#: lets the compiler, VM and disassembler stay in sync.
OPCODES: Dict[str, int] = {
    "NOP": 0,
    "LOAD_CONST": 1,
    "LOAD_NAME": 2,
    "STORE_NAME": 3,
    "POP": 4,
    "DUP": 5,
    "BUILD_LIST": 6,
    "LOAD_INDEX": 7,
    "STORE_INDEX": 8,
    "BINARY": 9,
    "UNARY": 10,
    "COMPARE": 11,
    "JUMP": 12,
    "JUMP_IF_FALSE": 13,
    "JUMP_IF_TRUE": 14,
    "CALL": 15,
    "RETURN": 16,
    "MAKE_FUNCTION": 17,
    "PRINT": 18,
    "HALT": 19,
    "BUILD_DICT": 20,
    "LOAD_SLICE": 21,
}

#: Ops whose ``arg`` is a jump target.
JUMP_OPS = frozenset({"JUMP", "JUMP_IF_FALSE", "JUMP_IF_TRUE"})

#: Binary operators accepted by ``BINARY``.
BINARY_OPS = frozenset({"+", "-", "*", "/", "%", "**"})
UNARY_OPS = frozenset({"-", "+", "not"})
COMPARE_OPS = frozenset({"==", "!=", "<", "<=", ">", ">="})


@dataclass
class Instruction:
    """One bytecode instruction.

    ``arg`` is a constant, a name, an operator, an argument count, or a jump
    target, depending on ``op``.  ``line`` is the source line used for
    diagnostics.
    """

    op: str
    arg: Any = None
    line: int = 0

    def __post_init__(self) -> None:
        if self.op not in OPCODES:
            raise BytecodeError("अमान्य ऑपकोड %r" % (self.op,), line=self.line)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"op": self.op, "line": self.line}
        if self.arg is not None:
            if isinstance(self.arg, CodeObject):
                data["code"] = self.arg.to_dict()
            else:
                data["arg"] = self.arg
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Instruction":
        if not isinstance(data, dict) or "op" not in data:
            raise BytecodeError("अमान्य निर्देश: %r" % (data,))
        arg: Any = data.get("arg")
        if "code" in data:
            arg = CodeObject.from_dict(data["code"])
        return cls(op=data["op"], arg=arg, line=int(data.get("line", 0)))


@dataclass
class CodeObject:
    """A compiled chunk: a module body or a function body."""

    name: str = "<module>"
    params: List[str] = field(default_factory=list)
    instructions: List[Instruction] = field(default_factory=list)
    source_name: str = "<input>"

    # -- building --------------------------------------------------------
    def emit(self, op: str, arg: Any = None, line: int = 0) -> int:
        """Append an instruction and return its index."""
        self.instructions.append(Instruction(op=op, arg=arg, line=line))
        return len(self.instructions) - 1

    def __len__(self) -> int:
        return len(self.instructions)

    # -- serialisation ---------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "params": list(self.params),
            "source": self.source_name,
            "instructions": [instr.to_dict() for instr in self.instructions],
        }

    @classmethod
    def from_dict(cls, data: Any) -> "CodeObject":
        if not isinstance(data, dict):
            raise BytecodeError("CodeObject अपेक्षित था")
        instructions = data.get("instructions", [])
        if not isinstance(instructions, list):
            raise BytecodeError("'instructions' सूची होनी चाहिए")
        code = cls(
            name=str(data.get("name", "<module>")),
            params=[str(p) for p in data.get("params", [])],
            source_name=str(data.get("source", "<input>")),
        )
        code.instructions = [Instruction.from_dict(item) for item in instructions]
        code.validate()
        return code

    # -- validation ------------------------------------------------------
    def validate(self) -> "CodeObject":
        """Check structural invariants; raise :class:`BytecodeError`."""
        total = len(self.instructions)
        for index, instr in enumerate(self.instructions):
            if instr.op in JUMP_OPS:
                target = instr.arg
                if not isinstance(target, int) or isinstance(target, bool):
                    raise BytecodeError(
                        "%s का लक्ष्य पूर्णांक होना चाहिए" % instr.op, line=instr.line
                    )
                if target < 0 or target > total:
                    raise BytecodeError(
                        "जम्प लक्ष्य सीमा से बाहर: %d" % target, line=instr.line
                    )
            elif instr.op == "CALL":
                if not isinstance(instr.arg, int) or instr.arg < 0:
                    raise BytecodeError("CALL की आर्ग्युमेंट संख्या अमान्य", line=instr.line)
            elif instr.op == "BUILD_LIST":
                if not isinstance(instr.arg, int) or instr.arg < 0:
                    raise BytecodeError("BUILD_LIST का आकार अमान्य", line=instr.line)
            elif instr.op == "BUILD_DICT":
                if not isinstance(instr.arg, int) or instr.arg < 0:
                    raise BytecodeError("BUILD_DICT का आकार अमान्य", line=instr.line)
            elif instr.op == "BINARY" and instr.arg not in BINARY_OPS:
                raise BytecodeError("अमान्य बाइनरी ऑपरेटर %r" % (instr.arg,), line=instr.line)
            elif instr.op == "UNARY" and instr.arg not in UNARY_OPS:
                raise BytecodeError("अमान्य यूनरी ऑपरेटर %r" % (instr.arg,), line=instr.line)
            elif instr.op == "COMPARE" and instr.arg not in COMPARE_OPS:
                raise BytecodeError("अमान्य तुलना ऑपरेटर %r" % (instr.arg,), line=instr.line)
            elif instr.op == "MAKE_FUNCTION" and not isinstance(instr.arg, CodeObject):
                raise BytecodeError("MAKE_FUNCTION को CodeObject चाहिए", line=instr.line)
        return self


def dump_bytecode(code: CodeObject, path: Optional[str] = None) -> bytes:
    """Serialise ``code``; optionally write it to ``path``."""
    code.validate()
    payload = json.dumps(
        {"format": FORMAT_NAME, "version": FORMAT_VERSION, "entry": code.to_dict()},
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
    ).encode("utf-8")
    blob = MAGIC + payload
    if path is not None:
        with open(path, "wb") as handle:
            handle.write(blob)
    return blob


def load_bytecode(source) -> CodeObject:
    """Load bytecode from a path, bytes or file-like object."""
    if hasattr(source, "read"):
        blob = source.read()
    elif isinstance(source, (bytes, bytearray)):
        blob = bytes(source)
    else:
        with open(source, "rb") as handle:
            blob = handle.read()

    if blob.startswith(MAGIC):
        blob = blob[len(MAGIC) :]
    try:
        data = json.loads(blob.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise BytecodeError("बाइटकोड पढ़ा नहीं जा सका: %s" % exc)

    if not isinstance(data, dict) or data.get("format") != FORMAT_NAME:
        raise BytecodeError("यह BRAHMA बाइटकोड नहीं है")
    version = data.get("version")
    if version != FORMAT_VERSION:
        raise BytecodeError(
            "असमर्थित बाइटकोड संस्करण %r (समर्थित: %d)" % (version, FORMAT_VERSION)
        )
    return CodeObject.from_dict(data.get("entry"))


def disassemble(code: CodeObject, indent: str = "") -> str:
    """Return a readable listing of ``code`` and any nested functions."""
    lines: List[str] = []
    header = "%s== %s" % (indent, code.name)
    if code.params:
        header += "(%s)" % ", ".join(code.params)
    lines.append(header)
    for index, instr in enumerate(code.instructions):
        arg = "" if instr.arg is None else " %s" % _format_arg(instr.arg)
        lines.append("%s%4d  %-16s%s" % (indent, index, instr.op, arg))
        if instr.op == "MAKE_FUNCTION" and isinstance(instr.arg, CodeObject):
            lines.append(disassemble(instr.arg, indent + "    "))
    return "\n".join(lines)


def _format_arg(arg: Any) -> str:
    if isinstance(arg, str):
        return repr(arg)
    return str(arg)


# ---------------------------------------------------------------------------
# Boot images
# ---------------------------------------------------------------------------
#: Signature of a bootable सूत्र-OS image.  Kept here (in the canonical package)
#: so that ``brahma_bytecode`` and ``brahma_llm.kernel`` cannot drift apart.
IMAGE_SIGNATURE = b"SUTRAOS"
IMAGE_VERSION = 1


def pack_image(payload: bytes, version: int = IMAGE_VERSION) -> bytes:
    """Wrap a bytecode payload: signature + version + length + payload."""
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("image payload बाइट्स होना चाहिए")
    return b"".join([
        IMAGE_SIGNATURE,
        struct.pack(">I", version),
        struct.pack(">I", len(payload)),
        bytes(payload),
    ])


def unpack_image(image: bytes) -> Tuple[int, bytes]:
    """Inverse of :func:`pack_image`; returns ``(version, payload)``."""
    if not isinstance(image, (bytes, bytearray)):
        raise TypeError("image बाइट्स होना चाहिए")
    if not image.startswith(IMAGE_SIGNATURE):
        raise ValueError("अमान्य image signature")
    head = len(IMAGE_SIGNATURE)
    if len(image) < head + 8:
        raise ValueError("अधूरा image header")
    version, size = struct.unpack(">II", image[head:head + 8])
    payload = bytes(image[head + 8:head + 8 + size])
    if len(payload) != size:
        raise ValueError("अधूरा image: %d बाइट चाहिए, मिले %d" % (size, len(payload)))
    return version, payload
