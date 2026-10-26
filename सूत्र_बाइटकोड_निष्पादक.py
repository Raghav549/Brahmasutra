
class बाइटकोडनिष्पादक:

    def __init__(self):

        self.memory = {}

    def निष्पादन(self, file):

        with open(file, "r", encoding="utf-8") as f:

            lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue

            opcode = int(parts[0])

            if opcode == 1:

                var = parts[1]
                value = int(parts[2])

                self.memory[var] = value

                print("स्थापित:", var, "=", value)

            elif opcode == 2:

                v1 = parts[1]
                v2 = parts[2]

                result = self.memory.get(v1, 0) + self.memory.get(v2, 0)

                self.memory[v1] = result

                print("योग:", v1, "=", result)

            elif opcode == 3:

                var = parts[1]

                print("दर्शय:", var, "=", self.memory.get(var, 0))

            else:

                print("अज्ञात opcode:", opcode)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ सूत्र बाइटकोड निष्पादक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
