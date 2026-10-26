

from ब्रह्म_प्रक्रिया_निष्पादन_कर्ण import ब्रह्मप्रक्रियानिष्पादनकर्ण


class ब्रह्मबहुप्रक्रियाकर्ण:


    def __init__(self):

        self.kernel = ब्रह्मप्रक्रियानिष्पादनकर्ण()

        self.queue = []


    def प्रक्रिया_निर्माण(self, नाम, आदेश):

        pid = self.kernel.निर्माण(नाम, आदेश)

        self.queue.append(pid)

        print("प्रक्रिया कतार में जोड़ी:", pid)

        return pid


    def अनुसूचन(self):

        print("अनुसूचक प्रारम्भ")

        while self.queue:

            pid = self.queue.pop(0)

            print("CPU प्रक्रिया चला रहा है:", pid)

            self.kernel.निष्पादन(pid)

        print("सभी प्रक्रियाएँ पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म बहु-प्रक्रिया कर्ण सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
