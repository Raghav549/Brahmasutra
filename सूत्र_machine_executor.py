# 🕉️ सूत्र Machine Code Executor

import सूत्र_parser as parser
import सूत्र_bytecode as bytecode
import सूत्र_machine_code as mc


class सूत्रMachineExecutor:

    def __init__(self):

        print("🕉️ सूत्र Machine Executor सक्रिय")

        self.registers = {}

        self.generator = mc.सूत्रMachineCodeGenerator()


    def run_file(self, filename):

        with open(filename, encoding="utf-8") as f:

            code = f.read()


        ast = parser.parse(code)

        bc = bytecode.generate(ast)

        machine = self.generator.generate(bc)

        self.execute(machine)


    def execute(self, machine):

        for instr in machine:

            opcode = instr[0]


            if opcode == 1:   # SET

                reg = instr[1]
                val = instr[2]

                self.registers[reg] = val

                print("स्थापित:", reg, "=", val)


            elif opcode == 2:  # ADD

                a = instr[1]
                b = instr[2]

                self.registers[a] = self.registers.get(a,0) + self.registers.get(b,0)

                print("योग:", a, "=", self.registers[a])


            elif opcode == 3:  # PRINT

                reg = instr[1]

                print("दर्शय:", reg, "=", self.registers.get(reg,0))


            elif opcode == 4:  # IMPORT

                module = instr[1]

                print("Module आयात:", module)


            elif opcode == 255: # EXIT

                print("निर्गम")
                break
