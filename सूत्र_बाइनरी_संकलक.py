# 🕉️ सूत्र बाइनरी संकलक

import सूत्र_parser
import सूत्र_bytecode
import सूत्र_मशीन_कोड_निर्माता
import सूत्र_द्विआधारी_निर्माता

class बाइनरीसंकलक:

    def __init__(self):

        self.parser = सूत्र_parser.Parser()

        self.bytecode = सूत्र_bytecode.BytecodeGenerator()

        self.machine = सूत्र_मशीन_कोड_निर्माता.मशीनकोडनिर्माता()

        self.binary = सूत्र_द्विआधारी_निर्माता.द्विआधारीनिर्माता()

    def संकलन(self,input_file,output_file):

        print("Parsing...")

        ast = self.parser.parse_file(input_file)

        print("Bytecode...")

        bytecode = self.bytecode.generate(ast)

        print("Machine code...")

        machine = self.machine.निर्मित(bytecode)

        print("Binary...")

        self.binary.निर्मित(machine,output_file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र बाइनरी संकलक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
