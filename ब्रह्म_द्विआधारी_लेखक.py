

class ब्रह्मद्विआधारीलेखक:


    def __init__(self):

        pass


    def लिखो(self, filename, program):

        with open(filename, "wb") as f:


            for inst in program:


                opcode = inst[0]

                op1 = inst[1]

                op2 = inst[2] if len(inst) > 2 else 0


                f.write(bytes([opcode]))
                f.write(bytes([op1]))
                f.write(bytes([op2]))


        print("Binary written:", filename)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म द्विआधारी लेखक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
