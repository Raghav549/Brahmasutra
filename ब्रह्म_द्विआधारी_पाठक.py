

class ब्रह्मद्विआधारीपाठक:


    def __init__(self):

        pass


    def पढ़ो(self, filename):

        program = []


        with open(filename, "rb") as f:


            data = f.read()


            for i in range(0, len(data), 3):


                opcode = data[i]
                op1 = data[i+1]
                op2 = data[i+2]


                program.append((opcode, op1, op2))


        print("Binary loaded:", filename)

        return program


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म द्विआधारी पाठक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
