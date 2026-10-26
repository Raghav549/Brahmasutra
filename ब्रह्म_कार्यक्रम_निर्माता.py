# ब्रह्म कार्यक्रम निर्माता v15

import os

from brahma_paths import data_root
class ब्रह्मकार्यक्रमनिर्माता:

    def __init__(self):

        self.output_dir = data_root("ब्रह्म_कार्यक्रम")

        os.makedirs(self.output_dir, exist_ok=True)

    def निर्माण(self, app_path, name):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return

        output_file = os.path.join(self.output_dir, name + ".कार्यक्रम")

        with open(output_file, "w", encoding="utf-8") as out:

            out.write("ब्रह्मकार्यक्रमV1\n")

            files = [
                "विन्यास.ब्रह्म",
                "पृष्ठभूमि.ब्रह्म",
                "अंतरफलक.ब्रह्म",
                "मुख्य.ब्रह्म"
            ]

            for file in files:

                full = os.path.join(app_path, file)

                if os.path.exists(full):

                    out.write("FILE_START\n")

                    with open(full, "r", encoding="utf-8") as f:

                        out.write(f.read())

                    out.write("\nFILE_END\n")

        print("कार्यक्रम निर्मित:", output_file)

        return output_file


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ ब्रह्म कार्यक्रम निर्माता सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
