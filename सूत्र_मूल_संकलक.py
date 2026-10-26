"""🕉️ सूत्र मूल संकलक — historical name for the assembler.

This module used to emit one 4-byte little-endian integer per *instruction*
(operands were thrown away), producing files that no machine could execute.
It now delegates to :class:`सूत्र_संकलक.संकलक`, i.e. to the single documented
format in :mod:`brahma_bytecode`.

>>> मूलसंकलक().अनुवाद("योग")
2
"""

from __future__ import annotations

import brahma_bytecode
from सूत्र_संकलक import संकलक


class मूलसंकलक(संकलक):
    """Backwards-compatible wrapper around :class:`सूत्र_संकलक.संकलक`."""

    def __init__(self) -> None:
        self.bytecode = bytearray()
        print("🕉️ सूत्र मूल संकलक सक्रिय")

    def संकलन(self, स्रोत: str, लक्ष्य: str):  # noqa: F811 - historical signature
        """Assemble ``स्रोत`` into ``लक्ष्य`` (same bytes as ``संकलक``)."""
        print(f"संकलन प्रारम्भ: {स्रोत}")
        code = brahma_bytecode.assemble_file(स्रोत, लक्ष्य)
        self.bytecode = bytearray(code)
        print(f"संकलन पूर्ण → {लक्ष्य}")
        return code

    def अनुवाद(self, आदेश: str):
        भाग = आदेश.split()
        if not भाग:
            return None
        if भाग[0] not in brahma_bytecode.OPCODES:
            raise brahma_bytecode.असेंबली_त्रुटि("अज्ञात आदेश %r" % भाग[0])
        return brahma_bytecode.OPCODES[भाग[0]]


__all__ = ["मूलसंकलक"]
