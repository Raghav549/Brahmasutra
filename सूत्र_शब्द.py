# 🕉️ BRAHMA VERSION 2
# सूत्र शब्द प्रणाली

from सूत्र_वर्ण import वर्णप्रणाली

class शब्दप्रणाली:

    def __init__(self):

        self.वर्ण = वर्णप्रणाली()

    def मान्य(self, शब्द):

        if len(शब्द) == 0:

            return False

        for अक्षर in शब्द:

            if not self.वर्ण.मान्य(अक्षर):

                return False

        return True


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global परीक्षण_सूची, प्रणाली, शब्द

    print("🕉️ सूत्र शब्द प्रणाली सक्रिय")
    प्रणाली = शब्दप्रणाली()

    परीक्षण_सूची = [
        "अ",
        "कर्म",
        "फल",
        "संख्या१",
        "_चर",
        "test",
        "abc",
        "१२३"
    ]

    print("शब्द परीक्षण:")

    for शब्द in परीक्षण_सूची:

        if प्रणाली.मान्य(शब्द):

            print(शब्द, "मान्य")

        else:

            print(शब्द, "अमान्य")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
