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


print("🕉️ सूत्र बाइनरी संकलक सक्रिय")
