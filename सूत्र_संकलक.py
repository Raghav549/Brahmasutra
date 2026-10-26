"""🕉️ सूत्र संकलक (compiler).

The repository used to contain five compilers writing four incompatible
bytecode layouts.  All of them now assemble to the format documented in
:mod:`brahma_bytecode`, and the same module executes the result, so a compiled
``.यन्त्र`` file is guaranteed to run.

Names kept for compatibility with the existing demos::

    सूत्रसंकलक = संकलक
    संकलक().संकलन(...)   # historical name of संकलित(...)

>>> सूत्रसंकलक().संकलित  # doctest: +ELLIPSIS
<bound method संकलक.संकलित ...>
"""

from __future__ import annotations

import brahma_bytecode


class संकलक:
    """Assemble सूत्र source (a file or text) into bytecode."""

    #: मnemonic → opcode (mirrors :data:`brahma_bytecode.OPCODES`)
    OPCODES = dict(brahma_bytecode.OPCODES)

    #: register names
    REGISTERS = dict(brahma_bytecode.REGISTERS)

    def संकलित(self, input_file: str, output_file: str) -> bytes:
        """Assemble ``input_file`` into ``output_file``; return the bytecode."""
        print("संकलन प्रारम्भ:", input_file)
        code = brahma_bytecode.assemble_file(input_file, output_file)
        print("🕉️ संकलन सफल:", output_file)
        return code

    def संकलित_पाठ(self, पाठ: str) -> bytes:
        """Assemble सूत्र source text (no files involved)."""
        return brahma_bytecode.assemble(पाठ)

    def अनुवाद(self, आदेश: str):
        """Translate a single mnemonic to its opcode (``None`` when empty)."""
        भाग = आदेश.split()
        if not भाग:
            return None
        if भाग[0] not in self.OPCODES:
            raise brahma_bytecode.असेंबली_त्रुटि("अज्ञात आदेश %r" % भाग[0])
        return self.OPCODES[भाग[0]]


#: ``संकलन-परीक्षण.py`` calls ``संकलक.संकलन()``; that name predates ``संकलित``.
संकलक.संकलन = संकलक.संकलित  # type: ignore[attr-defined]

#: historical alias
सूत्रसंकलक = संकलक

__all__ = ["संकलक", "सूत्रसंकलक"]
