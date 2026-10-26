# 🕉️ सूत्र पूर्ण संकलक

import सूत्र_parser
import सूत्र_bytecode
import सूत्र_मशीन_कोड_निर्माता

class पूर्णसंकलक:

    def __init__(self):

        self.parser = सूत्र_parser.Parser()
        self.bytecode_gen = सूत्र_bytecode.BytecodeGenerator()
        self.machine_gen = सूत्र_मशीन_कोड_निर्माता.मशीनकोडनिर्माता()

    def संकलन(self, input_file, output_file):

        print("Parsing...")

        ast = self.parser.parse_file(input_file)

        print("Bytecode generation...")

        bytecode = self.bytecode_gen.generate(ast)

        print("Machine code generation...")

        machine = self.machine_gen.निर्मित(bytecode)

        with open(output_file,"w") as f:

            for line in machine:
                f.write(line+"\n")

        print("संकलन पूर्ण:", output_file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र पूर्ण संकलक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
