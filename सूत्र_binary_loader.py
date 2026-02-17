# 🕉️ सूत्र Binary Loader

class सूत्रBinaryLoader:

    def __init__(self):

        print("🕉️ सूत्र Binary Loader सक्रिय")


    def load(self, filename):

        machine_code = []

        with open(filename, "rb") as f:

            while True:

                opcode = f.read(1)

                if not opcode:
                    break

                op1 = f.read(1)
                op2 = f.read(2)

                instruction = [

                    int.from_bytes(opcode, "big"),
                    int.from_bytes(op1, "big"),
                    int.from_bytes(op2, "big")

                ]

                machine_code.append(instruction)

        return machine_code
