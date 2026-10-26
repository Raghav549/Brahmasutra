

class ब्रह्मCPUकर्ण:

    def __init__(self):

        # CPU registers
        self.registers = {

            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0

        }

        self.program_counter = 0


    def स्थापित(self, नाम, मान):

        self.registers[नाम] = मान

        print("CPU स्थापित:", नाम, "=", मान)


    def प्राप्त(self, नाम):

        return self.registers.get(नाम, 0)


    def योग(self, अ, ब):

        परिणाम = self.registers.get(अ, 0) + self.registers.get(ब, 0)

        self.registers[अ] = परिणाम

        print("CPU योग:", अ, "=", परिणाम)


    def स्थिति(self):

        print("CPU Registers:")

        for k, v in self.registers.items():

            print(k, "=", v)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म CPU कर्ण सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
