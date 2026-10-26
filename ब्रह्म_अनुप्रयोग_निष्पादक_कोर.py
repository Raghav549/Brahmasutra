# 🕉️ ब्रह्म अनुप्रयोग निष्पादक कोर
# VERSION 8

import os


class ब्रह्मअनुप्रयोगनिष्पादककोर:

    def __init__(self):

        self.चर = {}

        print("निष्पादक तैयार")


    def स्थापित(self, नाम, मान):

        self.चर[नाम] = int(मान)

        print(f"स्थापित: {नाम} = {मान}")


    def दर्शय(self, नाम):

        if नाम in self.चर:

            print(f"दर्शय: {नाम} = {self.चर[नाम]}")

        else:

            print("त्रुटि: चर नहीं मिला")


    def योग(self, अ, ब):

        if अ in self.चर and ब in self.चर:

            self.चर[अ] += self.चर[ब]

            print(f"योग: {अ} = {self.चर[अ]}")

        else:

            print("त्रुटि: चर नहीं मिला")


    def आदेश_चलाओ(self, line):

        parts = line.strip().split()

        if len(parts) == 0:
            return

        cmd = parts[0]


        if cmd == "स्थापित":

            self.स्थापित(parts[1], parts[2])


        elif cmd == "दर्शय":

            self.दर्शय(parts[1])


        elif cmd == "योग":

            self.योग(parts[1], parts[2])


        else:

            print("अमान्य आदेश:", cmd)


    def निष्पादन(self, file_path):

        if not os.path.exists(file_path):

            print("त्रुटि: संचिका नहीं मिली")
            return

        print("अनुप्रयोग निष्पादन प्रारम्भ")

        with open(file_path, "r", encoding="utf-8") as f:

            for line in f:

                self.आदेश_चलाओ(line)

        print("अनुप्रयोग निष्पादन पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global executor, test_file

    print("🕉️ ब्रह्म अनुप्रयोग निष्पादक कोर सक्रिय")
    executor = ब्रह्मअनुप्रयोगनिष्पादककोर()

    test_file = os.path.expanduser("~/सूत्र-तंत्र/परीक्षण.ब्रह्म")

    executor.निष्पादन(test_file)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
