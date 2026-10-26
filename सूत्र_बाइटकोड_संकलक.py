
class बाइटकोडसंकलक:

    def __init__(self):
        self.opcodes = {
            "संकल्प": 1,
            "योग": 2,
            "दर्शय": 3
        }

    def संकलन(self, input_file, output_file):

        bytecode = []

        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            cmd = parts[0]

            if cmd not in self.opcodes:
                print("अमान्य आदेश:", cmd)
                continue

            opcode = self.opcodes[cmd]

            instruction = [opcode]

            for p in parts[1:]:
                instruction.append(p)

            bytecode.append(instruction)

        with open(output_file, "w", encoding="utf-8") as f:

            for instr in bytecode:

                f.write(" ".join(map(str, instr)) + "\n")

        print("संकलन पूर्ण:", output_file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ सूत्र बाइटकोड संकलक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
