

from ब्रह्म_बूट_लोडर import ब्रह्मबूटलोडर


class ब्रह्मसिस्टम:


    def __init__(self):

        print("BRAHMA SYSTEM POWER ON")

        self.bootloader = ब्रह्मबूटलोडर()


    def प्रारम्भ(self):

        print("SYSTEM START")

        filename = input("Enter binary filename: ")

        self.bootloader.बूट(filename)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म सिस्टम प्रारम्भ")


if __name__ == "__main__":
    _main()
