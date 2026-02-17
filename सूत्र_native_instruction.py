# 🕉️ सूत्र Native Instruction Layer

class सूत्रNativeInstruction:


    def __init__(self):

        print("🕉️ सूत्र Native Instruction Layer सक्रिय")

        self.instructions = []


    def जोड़ो(self, opcode, operand1=None, operand2=None):

        instruction = {

            "opcode": opcode,

            "op1": operand1,

            "op2": operand2

        }

        self.instructions.append(instruction)

        print("Native Instruction जोड़ा:", instruction)


    def सूची(self):

        return self.instructions
