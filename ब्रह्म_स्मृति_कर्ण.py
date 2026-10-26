
class ब्रह्मस्मृतिकर्ण:

    def __init__(self):

        self.स्मृति = {}

        self.अगला_पता = 1000


    def आवंटन(self, मान):

        पता = self.अगला_पता

        self.स्मृति[पता] = मान

        self.अगला_पता += 1

        print("स्मृति आवंटित:", पता, "=", मान)

        return पता


    def लेखन(self, पता, मान):

        if पता in self.स्मृति:

            self.स्मृति[पता] = मान

            print("स्मृति लेखन:", पता, "=", मान)


    def पठन(self, पता):

        if पता in self.स्मृति:

            मान = self.स्मृति[पता]

            print("स्मृति पठन:", पता, "=", मान)

            return मान

        return None


    def स्थिति(self):

        print("स्मृति स्थिति:")

        for पता, मान in self.स्मृति.items():

            print(पता, "=", मान)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global p1, p2, ram
    print("🕉️ ब्रह्म स्मृति कर्ण सक्रिय")
    ram = ब्रह्मस्मृतिकर्ण()

    p1 = ram.आवंटन(100)

    p2 = ram.आवंटन(200)

    ram.लेखन(p1, 500)

    ram.पठन(p1)

    ram.स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
