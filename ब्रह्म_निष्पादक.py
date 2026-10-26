# ब्रह्म निष्पादक v11 FINAL FIX

import os

class ब्रह्मनिष्पादक:

    def __init__(self):
        print("ब्रह्म निष्पादक सक्रिय")
        self.चर = {}

    def संचिका_खोज(self, नाम):

        # direct path
        if os.path.isfile(नाम):
            return नाम

        # current directory
        path = os.path.join(os.getcwd(), नाम)
        if os.path.isfile(path):
            return path

        # ब्रह्म अनुप्रयोग folder
        base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_अनुप्रयोग")
        path = os.path.join(base, नाम)
        if os.path.isfile(path):
            return path

        return None


    def निष्पादन(self, नाम):

        path = self.संचिका_खोज(नाम)

        if path is None:
            print("त्रुटि: संचिका नहीं मिली")
            return

        print("निष्पादन प्रारम्भ:", path)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            parts = line.split()

            if parts[0] == "स्थापित":

                var = parts[1]
                value = int(parts[2])

                self.चर[var] = value

                print("स्थापित:", var, "=", value)


            elif parts[0] == "योग":

                a = parts[1]
                b = parts[2]

                self.चर[a] = self.चर.get(a,0) + self.चर.get(b,0)

                print("योग:", a, "=", self.चर[a])


            elif parts[0] == "दर्शय":

                var = parts[1]

                print("दर्शय:", var, "=", self.चर.get(var,0))


        print("निष्पादन पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ ब्रह्म पुनरावृत्ति प्रणाली सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
