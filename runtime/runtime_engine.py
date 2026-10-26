import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

from vm.sutra_vm import सूत्रVM

MAGIC = "SUTRA_BIN_V1"

class सूत्रRuntime:

    def __init__(self):

        self.vm = सूत्रVM()

        self.loaded_program = None

    def लोड(self, file):

        print("कार्यक्रम लोड हो रहा है...")

        with open(file, encoding="utf-8") as f:

            first = f.readline().strip()

            if first == MAGIC:

                self.loaded_program = file

            else:

                raise Exception("अमान्य binary format")

    def प्रारंभ(self):

        if not self.loaded_program:

            print("कोई कार्यक्रम नहीं")

            return

        print("कार्यक्रम प्रारंभ")

        self.vm.bytecode_चलाओ(self.loaded_program)

        print("कार्यक्रम समाप्त")
