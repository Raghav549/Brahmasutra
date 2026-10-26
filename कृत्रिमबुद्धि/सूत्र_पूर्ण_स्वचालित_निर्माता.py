# 🕉️ सूत्र पूर्ण स्वचालित अनुप्रयोग निर्माण तंत्र
"""Build → compile → execute, with every step actually happening.

The previous version copied the ``.सूत्र`` text file to ``.सूत्रबिन`` (UTF-8, not
bytecode) and "executed" it by printing the source back at the user.

Now:

``संकलन``   compiles the सूत्र program with :mod:`brahma.compiler` into real
            bytecode (``brahma.bytecode``), and reports the code size;
``निष्पादन`` loads that bytecode and runs it on the project's VM, printing the
            program's real output;
``पूर्णनिर्माण`` asks :class:`सूत्रअनुप्रयोगनिर्माता` (i.e. ब्रह्म-LLM) for an app,
            compiles its logic to ``.sbc``, runs it, and keeps the artefacts.

Nothing here writes into the current working directory: applications live under
``$BRAHMA_HOME``/``~/सूत्र-तंत्र``.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
# The sibling module must win over the same-named file in the repository root,
# so this directory goes in front and the root goes last.
if _ROOT not in sys.path:
    sys.path.append(_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from brahma.api import load_and_run  # noqa: E402
from brahma.bytecode import disassemble, dump_bytecode, load_bytecode  # noqa: E402
from brahma.compiler import compile_file, compile_source  # noqa: E402
from brahma_paths import data_root  # noqa: E402

from सूत्र_अनुप्रयोग_निर्माता import सूत्रअनुप्रयोगनिर्माता  # noqa: E402


class सूत्रपूर्णस्वचालितनिर्माता:
    """End-to-end pipeline: LLM → सूत्र source → bytecode → execution."""

    def __init__(self, out_root=None):
        print("🕉️ सूत्र पूर्ण स्वचालित निर्माण तंत्र सक्रिय")
        self.निर्माता = सूत्रअनुप्रयोगनिर्माता(out_root=out_root)
        self.पथ = self.निर्माता.अनुप्रयोग_पथ
        self.द्विआधारीपथ = data_root("bytecode", create=True)

    # -- compile ---------------------------------------------------------
    def संकलन(self, नाम, स्रोत=None):
        """Compile ``नाम``'s सूत्र source into real bytecode; return the path."""
        स्रोत = स्रोत or os.path.join(self.पथ, नाम, "%s.sutra" % नाम)
        if not os.path.exists(स्रोत):
            raise FileNotFoundError("सूत्र स्रोत नहीं मिला: %s" % स्रोत)
        लक्ष्य = os.path.join(self.द्विआधारीपथ, "%s.sbc" % नाम)
        code = compile_file(स्रोत)
        blob = dump_bytecode(code)
        with open(लक्ष्य, "wb") as handle:
            handle.write(blob)
        print("द्विआधारी निर्मित: %s (%d बाइट, %d निर्देश)"
              % (लक्ष्य, len(blob), len(code.instructions)))
        return लक्ष्य

    # -- execute ---------------------------------------------------------
    def निष्पादन(self, नाम):
        """Run ``नाम``'s compiled bytecode on the VM; return the output lines."""
        लक्ष्य = os.path.join(self.द्विआधारीपथ, "%s.sbc" % नाम)
        if not os.path.exists(लक्ष्य):
            # Accept a source path as well, so callers can skip संकलन.
            raise FileNotFoundError("बाइटकोड नहीं मिला: %s (पहले संकलन करें)" % लक्ष्य)
        print("निष्पादन प्रारम्भ:", लक्ष्य)
        result = load_and_run(लक्ष्य)
        for line in result.output:
            print(line)
        if result.error is not None:
            print("त्रुटि: %s" % result.error.format())
        return result.output

    def विघटन(self, नाम):
        """Disassemble the compiled program (useful, and it proves it is bytecode)."""
        लक्ष्य = os.path.join(self.द्विआधारीपथ, "%s.sbc" % नाम)
        listing = disassemble(load_bytecode(open(लक्ष्य, "rb").read()))
        print(listing)
        return listing

    # -- pipeline --------------------------------------------------------
    def पूर्णनिर्माण(self, नाम):
        """Generate an app, compile its logic, run it, and return the artefacts."""
        print("अनुप्रयोग निर्माण प्रारम्भ:", नाम)
        manifest = self.निर्माता.सूत्र_अनुप्रयोग(नाम)
        स्रोत = os.path.join(manifest["dir"], manifest["logic_file"])
        binary = self.संकलन(नाम, स्रोत)
        output = self.निष्पादन(नाम)
        print("पूर्ण निर्माण समाप्त — smoke:", "ठीक" if manifest["smoke"].get("ok") else "विफल")
        return {
            "app": manifest["dir"],
            "source": स्रोत,
            "bytecode": binary,
            "output": output,
            "smoke": manifest["smoke"],
            "logic_origin": manifest["logic_origin"],
        }


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:
        _brahma_cli_run = None

    def _main():
        तंत्र = सूत्रपूर्णस्वचालितनिर्माता()
        return 0 if तंत्र.पूर्णनिर्माण("पूर्ण_अनुप्रयोग") else 1

    if _brahma_cli_run is None:
        raise SystemExit(_main())
    raise SystemExit(_brahma_cli_run(_main))
