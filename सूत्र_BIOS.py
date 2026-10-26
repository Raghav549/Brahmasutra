# 🕉️ सूत्र BIOS प्रणाली

from सूत्र_मूलपटल import सूत्रमूलपटल


class सूत्रBIOS:

    def __init__(self):

        print("🕉️ सूत्र BIOS सक्रिय")

        self.board = None


    def शक्ति_आरम्भ(self):

        print("शक्ति चालू")
        print("हार्डवेयर परीक्षण...")


    def हार्डवेयर_जाँच(self):

        print("CPU जाँच सफल")
        print("RAM जाँच सफल")
        print("BUS जाँच सफल")
        print("भण्डारण जाँच सफल")


    def मूलपटल_सक्रिय(self):

        print("मूलपटल सक्रिय हो रहा है")

        self.board = सूत्रमूलपटल()


    def बूट_लोड(self, file):

        print("Bootloader प्रारम्भ")

        if self.board is None:

            print("त्रुटि: मूलपटल सक्रिय नहीं")

            return

        self.board.चलाओ(file)


    def प्रारम्भ(self, file):

        print("🕉️ सूत्र BIOS प्रारम्भ")

        self.शक्ति_आरम्भ()

        self.हार्डवेयर_जाँच()

        self.मूलपटल_सक्रिय()

        self.बूट_लोड(file)

        print("🕉️ BIOS प्रक्रिया पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global bios
    bios = सूत्रBIOS()

    bios.प्रारम्भ("test.यन्त्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
