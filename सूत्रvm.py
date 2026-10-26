# सूत्र तंत्र — Virtual Machine
# Bytecode Execution Engine

import json


class सूत्रVM:

    def __init__(self):
        self.memory = {}

    def run(self, bytecode_file):

        with open(bytecode_file, "r", encoding="utf-8") as f:
            program = json.load(f)

        for instruction in program:

            opcode = instruction["opcode"]

            if opcode == "SET":

                name = instruction["name"]
                value = instruction["value"]

                self.memory[name] = value

            elif opcode == "PRINT":

                name = instruction["name"]

                if name in self.memory:
                    print("फल:", self.memory[name])
                else:
                    print("त्रुटि: अपरिभाषित", name)


def परीक्षण():

    print("सूत्र VM सक्रिय")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    परीक्षण()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
