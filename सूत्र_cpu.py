# सूत्र CPU with Module system

import सूत्र_parser as parser
import सूत्र_bytecode as bytecode


class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र CPU सक्रिय")

        self.registers = {}


    def execute(self, code):

        for instr in code:

            op = instr[0]


            if op == "SET":

                self.registers[instr[1]] = instr[2]

                print("स्थापित:", instr[1], "=", instr[2])


            elif op == "ADD":

                a = instr[1]
                b = instr[2]

                self.registers[a] = self.registers.get(a,0) + self.registers.get(b,0)

                print("योग:", a, "=", self.registers[a])


            elif op == "PRINT":

                print(instr[1], "=", self.registers.get(instr[1],0))


            elif op == "IMPORT":

                module_name = instr[1]

                print("Module आयात:", module_name)

                try:

                    with open("modules/" + module_name + ".सूत्र", encoding="utf-8") as f:

                        module_code = f.read()

                    ast = parser.parse(module_code)

                    bc = bytecode.generate(ast)

                    self.execute(bc)

                except:

                    print("Module नहीं मिला:", module_name)


            elif op == "EXIT":

                print("निर्गम")
                break
