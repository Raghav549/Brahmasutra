# 🕉️ सूत्र आभासी CPU


class आभासीCPU:


    def __init__(self):

        self.register = {

            1: 0,
            2: 0,
            3: 0,
            4: 0

        }

        print("🕉️ सूत्र आभासी CPU सक्रिय")


    def चलाओ(self, bytecode_file):

        with open(bytecode_file, "rb") as f:

            code = list(f.read())


        pc = 0


        while pc < len(code):

            opcode = code[pc]

            pc += 1


            # संकल्प
            if opcode == 1:

                reg = code[pc]
                val = code[pc+1]

                pc += 2

                self.register[reg] = val

                print(f"स्थापित: {reg} = {val}")


            # योग
            elif opcode == 2:

                r1 = code[pc]
                r2 = code[pc+1]

                pc += 2

                self.register[r1] += self.register[r2]

                print(f"योग परिणाम: {r1} = {self.register[r1]}")


            # दर्शय
            elif opcode == 3:

                reg = code[pc]

                pc += 1

                print(f"रजिस्टर {reg} = {self.register[reg]}")


            # निर्गम
            elif opcode == 4:

                print("🕉️ प्रोग्राम समाप्त")

                break


            else:

                print("अज्ञात opcode:", opcode)

                break
