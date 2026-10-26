# 🕉️ ब्रह्म Runtime कोर
# VERSION 10

import os

from ब्रह्म_अनुप्रयोग_लोडर_कोर import ब्रह्मअनुप्रयोगलोडरकोर


class ब्रह्मRuntimeकोर:

    def __init__(self):

        self.loader = ब्रह्मअनुप्रयोगलोडरकोर()

        self.running = False

        print("Runtime तैयार")


    def प्रारम्भ(self, अनुप्रयोग):

        print("Runtime प्रारम्भ")

        self.running = True

        self.loader.निष्पादन(अनुप्रयोग)

        print("Runtime समाप्त")

        self.running = False


    def स्थिति(self):

        if self.running:

            print("Runtime स्थिति: सक्रिय")

        else:

            print("Runtime स्थिति: निष्क्रिय")


    def रोक(self):

        print("Runtime रोक दिया गया")

        self.running = False


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global runtime


    print("🕉️ ब्रह्म Runtime कोर सक्रिय")
    runtime = ब्रह्मRuntimeकोर()

    runtime.स्थिति()

    runtime.प्रारम्भ("परीक्षण.ब्रह्म")

    runtime.स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
