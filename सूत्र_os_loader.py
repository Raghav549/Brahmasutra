"""🕉️ सूत्र OS Loader — boot image loader.

``run_program`` used to call ``सूत्रBinaryLoader.load_and_run`` — a method that
did not exist — so every program run through the OS loader crashed.  It now
executes the documented सूत्र bytecode from :mod:`brahma_bytecode`, and also
accepts a ``.img`` boot image (see :func:`brahma_bytecode.unpack_image`).

>>> सूत्रOSLoader(verbose=False).run_program(  # doctest: +ELLIPSIS
...     __import__("io").BytesIO(b"\\x01\\x01\\x00\\x00\\x00\\x07\\x06"))
स्थापित: अ = 7
{'अ': 7}
"""

from __future__ import annotations

import brahma_bytecode
from brahma_bytecode import Machine


class सूत्रOSLoader:
    """Load and execute bytecode programs or boot images."""

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose
        if verbose:
            print("🕉️ सूत्र Operating System Loader सक्रिय")

    def run_program(self, स्रोत):
        """Execute ``स्रोत`` (path, bytes or file object); return registers."""
        if self.verbose:
            print("OS program execution प्रारम्भ")

        if hasattr(स्रोत, "read"):
            data = स्रोत.read()
        elif isinstance(स्रोत, (bytes, bytearray)):
            data = bytes(स्रोत)
        else:
            with open(स्रोत, "rb") as handle:
                data = handle.read()

        if data.startswith(brahma_bytecode.IMAGE_SIGNATURE):
            version, data = brahma_bytecode.unpack_image(data)
            if self.verbose:
                print("Boot image version:", version)

        registers = Machine(verbose=self.verbose).run(data)

        if self.verbose:
            print("OS execution समाप्त")
        return registers

    #: ``सूत्र_boot_simulator.py`` calls ``चलाओ``; ``run_program`` is the older name.
    def चलाओ(self, स्रोत):
        """Alias of :meth:`run_program`."""
        return self.run_program(स्रोत)


# Compatibility alias — ``सूत्र_boot_simulator.py`` imports ``OSLoader``.
OSLoader = सूत्रOSLoader

__all__ = ["सूत्रOSLoader", "OSLoader"]
