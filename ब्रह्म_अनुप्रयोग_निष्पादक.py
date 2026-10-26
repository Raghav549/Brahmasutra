# ब्रह्म अनुप्रयोग निष्पादक v14

import os

from ब्रह्म_निष्पादक import ब्रह्मनिष्पादक

class ब्रह्मअनुप्रयोगनिष्पादक:

    def __init__(self):

        self.executor = ब्रह्मनिष्पादक()

    def निष्पादन(self, app_path):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return

        print("अनुप्रयोग प्रारम्भ:", app_path)

        files = [
            "विन्यास.ब्रह्म",
            "पृष्ठभूमि.ब्रह्म",
            "अंतरफलक.ब्रह्म",
            "मुख्य.ब्रह्म"
        ]

        for file in files:

            full = os.path.join(app_path, file)

            if os.path.exists(full):

                print("निष्पादन:", file)

                self.executor.निष्पादन(full)

        print("अनुप्रयोग समाप्त")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ ब्रह्म अनुप्रयोग निष्पादक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
