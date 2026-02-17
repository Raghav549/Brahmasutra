# 🕉️ सूत्र Binary Generator

class सूत्रBinaryGenerator:

    def __init__(self):

        print("🕉️ सूत्र Binary Generator सक्रिय")


    def save(self, machine_code, filename):

        with open(filename, "wb") as f:

            for instruction in machine_code:

                opcode = instruction[0]
                op1 = instruction[1]
                op2 = instruction[2]

                f.write(opcode.to_bytes(1, "big"))
                f.write(op1.to_bytes(1, "big"))
                f.write(op2.to_bytes(2, "big"))

        print("Binary file saved:", filename)
