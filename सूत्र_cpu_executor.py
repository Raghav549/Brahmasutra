# 🕉️ सूत्र CPU Executor


class सूत्रCPU:


    def __init__(self):

        self.register = {

            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0

        }


    def execute(self, binary_file):

        print("🕉️ सूत्र CPU निष्पादन प्रारम्भ")


        with open(binary_file, "rb") as f:

            code = list(f.read())


        # verify header
        if code[0:5] != [83,85,84,82,65]:

            print("त्रुटि: अमान्य binary")

            return


        i = 5


        while i < len(code):


            opcode = code[i]


            if opcode == 10:  # load

                reg = code[i+1]
                val = code[i+2]

                reg_name = list(self.register.keys())[reg]

                self.register[reg_name] = val

                print(f"स्थापित: {reg_name} = {val}")

                i += 3


            elif opcode == 20:  # add

                r1 = list(self.register.keys())[code[i+1]]

                r2 = list(self.register.keys())[code[i+2]]

                self.register[r1] += self.register[r2]

                print(f"योग: {r1} = {self.register[r1]}")

                i += 3


            elif opcode == 30:  # print

                r = list(self.register.keys())[code[i+1]]

                print(f"दर्शय: {r} = {self.register[r]}")

                i += 2


            elif opcode == 255:

                print("निर्गम")

                break


            else:

                i += 1


        print("CPU समाप्त")
