

from ब्रह्म_द्विआधारी_पाठक import ब्रह्मद्विआधारीपाठक
from ब्रह्म_मशीन_कर्ण import ब्रह्ममशीन


class ब्रह्मबूटलोडर:


    def __init__(self):

        print("BOOT SYSTEM READY")

        self.reader = ब्रह्मद्विआधारीपाठक()

        self.machine = ब्रह्ममशीन()


    def बूट(self, filename):

        print("BOOT START")

        program = self.reader.पढ़ो(filename)

        self.machine.लोड(program)

        self.machine.run()

        print("BOOT COMPLETE")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म बूट लोडर सक्रिय")


if __name__ == "__main__":
    _main()
