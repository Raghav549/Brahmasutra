# 🕉️ ब्रह्म AI निष्पादक VERSION 16
# पूर्ण निष्पादन तंत्र

import os


class ब्रह्मAINishpadak:

    def __init__(self):

        self.base_path = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

    def file_path(self, name):

        return os.path.join(
            self.base_path,
            name,
            "मुख्य.ब्रह्म"
        )

    def आदेश_चलाओ(self, line):

        parts = line.strip().split()

        if not parts:
            return

        command = parts[0]

        if command == "दर्शय":

            text = " ".join(parts[1:])

            print("OUTPUT:", text)

        elif command.startswith("कार्य"):

            return

        elif command == "मुख्य()":

            return

        elif command.endswith("()"):

            print("FUNCTION CALL:", command)

        else:

            print("UNKNOWN:", line)

    def निष्पादन(self, name):

        path = self.file_path(name)

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return

        print("अनुप्रयोग लोड:", path)

        with open(path, encoding="utf-8") as f:

            lines = f.readlines()

        print("निष्पादन प्रारम्भ")

        for line in lines:

            self.आदेश_चलाओ(line)

        print("निष्पादन पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global engine, name

    print("🕉️ ब्रह्म AI निष्पादक VERSION 16 सक्रिय")


    # run engine

    engine = ब्रह्मAINishpadak()

    name = input("अनुप्रयोग नाम लिखें: ")

    engine.निष्पादन(name)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
