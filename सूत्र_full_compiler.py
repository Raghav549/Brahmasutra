# 🕉️ सूत्र Full Compiler

import सूत्र_parser as parser
import सूत्र_bytecode as bytecode
import सूत्र_machine_code as machine
import सूत्र_binary_writer as writer


class सूत्रCompiler:

    def __init__(self):

        print("🕉️ सूत्र Compiler सक्रिय")

        self.generator = machine.सूत्रMachineCodeGenerator()

        self.writer = writer.सूत्रBinaryWriter()


    def compile(self, source, output):

        with open(source, encoding="utf-8") as f:

            code = f.read()


        ast = parser.parse(code)

        bc = bytecode.generate(ast)

        machine_code = self.generator.generate(bc)

        self.writer.write(machine_code, output)
