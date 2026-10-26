"""🕉️ सूत्र यन्त्र निष्पादक — execute सूत्र bytecode.

Bytecode is produced by ``सूत्र_संकलक`` / ``सूत्र-यन्त्र-संकलक`` and decoded by
:class:`brahma_bytecode.Machine`; the format is documented in
:mod:`brahma_bytecode`.  Bad input raises :class:`brahma_bytecode.असेंबली_त्रुटि`
instead of ``IndexError``/``KeyError`` escaping an interpreter loop.

>>> यन्त्रनिष्पादक().निष्पादन(बाइटकोड("संकल्प अ 7\\nदर्शय अ"))
स्थापित: अ = 7
दर्शय: अ = 7
{'अ': 7}
"""

from __future__ import annotations

import brahma_bytecode
from brahma_bytecode import Machine, असेंबली_त्रुटि


def बाइटकोड(पाठ: str) -> bytes:
    """Assemble सूत्र source text into bytecode (convenience for demos)."""
    return brahma_bytecode.assemble(पाठ)


class यन्त्रनिष्पादक:
    """Run bytecode files or bytes; keeps the registers between runs."""

    def __init__(self, verbose: bool = True) -> None:
        self.register = {}
        self.verbose = verbose

    def निष्पादन(self, स्रोत):
        """Execute ``स्रोत`` (path, bytes or an open binary file)."""
        if hasattr(स्रोत, "read"):
            code = स्रोत.read()
        elif isinstance(स्रोत, (bytes, bytearray)):
            code = bytes(स्रोत)
        else:
            with open(स्रोत, "rb") as handle:
                code = handle.read()

        machine = Machine(verbose=self.verbose)
        machine.registers.update(self.register)
        self.register = machine.run(code)
        return dict(self.register)

    #: ``यन्त्र-परीक्षण.py`` calls ``चलाओ``; ``निष्पादन`` is the older name.
    def चलाओ(self, स्रोत):
        """Alias of :meth:`निष्पादन`."""
        return self.निष्पादन(स्रोत)


#: Compatibility alias used by ``यन्त्र-परीक्षण.py``.
सूत्रयन्त्र = यन्त्रनिष्पादक

__all__ = ["यन्त्रनिष्पादक", "सूत्रयन्त्र", "बाइटकोड", "असेंबली_त्रुटि"]
