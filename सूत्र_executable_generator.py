# 🕉️ सूत्र Executable Generator


class सूत्रExecutableGenerator:


    def __init__(self):

        print("🕉️ सूत्र Executable Generator सक्रिय")


    def create(self, machine_code, filename):

        with open(filename, "wb") as f:

            # header
            f.write(b"SUTRA_EXEC_V1")

            for instruction in machine_code:

                opcode = instruction[0]
                op1 = instruction[1]
                op2 = instruction[2]

                f.write(opcode.to_bytes(1, "big"))
                f.write(op1.to_bytes(1, "big"))
                f.write(op2.to_bytes(2, "big"))

        print("Executable created:", filename)
