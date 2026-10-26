# सूत्र तंत्र — Native Machine Layer

class सूत्रNative:

    def __init__(self):

        self.स्मृति = [0] * 256

        self.रजिस्टर = {
            "क": 0,
            "ख": 0,
            "ग": 0,
            "घ": 0
        }


    def load(self, bytecode_file):

        with open(bytecode_file, "r") as f:

            self.instructions = f.readlines()


    def execute(self):

        pc = 0

        while pc < len(self.instructions):

            line = self.instructions[pc].strip()

            parts = line.split()

            if not parts:
                pc += 1
                continue


            आदेश = parts[0]


            if आदेश == "SET":

                reg = parts[1]

                value = int(parts[2])

                self.रजिस्टर[reg] = value

                print("रजिस्टर", reg, "=", value)


            elif आदेश == "ADD":

                reg = parts[1]

                value = int(parts[2])

                self.रजिस्टर[reg] += value

                print("रजिस्टर", reg, "=", self.रजिस्टर[reg])


            elif आदेश == "PRINT":

                reg = parts[1]

                print("फल:", self.रजिस्टर[reg])


            pc += 1


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global native
    native = सूत्रNative()

    native.load("test.sbc")

    native.execute()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
