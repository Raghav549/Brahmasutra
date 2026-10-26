"""🕉️ सूत्र Binary Loader — load a ``.बिन`` image and run it.

A ``.बिन`` file is a sequence of 4-byte records::

    opcode (1 byte) | operand1 (1 byte) | operand2 (2 bytes, big-endian)

The historical class only had ``load()``, while ``सूत्र_os_loader`` called
``load_and_run()`` — so every program that went through the OS loader crashed
with ``AttributeError``.  Both methods exist here, and malformed images raise
:class:`बाइन_त्रुटि` instead of silently producing nonsense instructions.

>>> loader = सूत्रBinaryLoader(verbose=False)
>>> loader.decode(b"\\x01\\x02\\x00\\x05")
[[1, 2, 5]]
"""

from __future__ import annotations

from typing import List, Optional

RECORD = 4


class बाइन_त्रुटि(Exception):
    """Malformed binary image."""


class सूत्रBinaryLoader:
    """Read 4-byte instruction records and execute them."""

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose
        if verbose:
            print("🕉️ सूत्र Binary Loader सक्रिय")

    # -- decoding --------------------------------------------------------
    @staticmethod
    def decode(data: bytes) -> List[List[int]]:
        """Split ``data`` into ``[opcode, operand1, operand2]`` records."""
        if len(data) % RECORD:
            raise बाइन_त्रुटि(
                "बाइन आकार %d बाइट है — 4 का गुणज होना चाहिए" % len(data)
            )
        return [
            [data[i], data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")]
            for i in range(0, len(data), RECORD)
        ]

    def load(self, filename) -> List[List[int]]:
        """Read ``filename`` and return its instruction list."""
        with open(filename, "rb") as handle:
            data = handle.read()
        return self.decode(data)

    # -- execution -------------------------------------------------------
    def load_and_run(self, filename) -> List[List[int]]:
        """Load and execute ``filename``; return the instruction list."""
        instructions = self.load(filename)
        self.execute(instructions)
        return instructions

    def execute(self, instructions: List[List[int]]) -> None:
        """Run decoded instructions against a small register bank."""
        registers = {}
        for opcode, operand1, operand2 in instructions:
            if opcode == 1:
                registers[operand1] = operand2
                if self.verbose:
                    print("लोड:", operand1, "=", operand2)
            elif opcode == 2:
                registers[operand1] = registers.get(operand1, 0) + registers.get(operand2, 0)
                if self.verbose:
                    print("योग:", operand1, "=", registers[operand1])
            elif opcode == 3:
                if self.verbose:
                    print("दर्शय:", operand1, "=", registers.get(operand1, 0))
            elif opcode == 4:
                break
            else:
                raise बाइन_त्रुटि("अज्ञात ऑपकोड %d" % opcode)


#: Compatibility alias.
बाइनलोडर = सूत्रBinaryLoader

__all__ = ["सूत्रBinaryLoader", "बाइनलोडर", "बाइन_त्रुटि"]
