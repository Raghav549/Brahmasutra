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


print("🕉️ सूत्र पूर्ण संकलक सक्रिय")
