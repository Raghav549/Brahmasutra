# 🕉️ सूत्र CPU v2 — Instruction Set Architecture

class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र CPU v2 सक्रिय")

        self.रजिस्टर = {
            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0
        }

        self.स्मृति = []

        self.IP = 0

        self.सक्रिय = False


    def स्मृति_लोड(self, instructions):

        print("स्मृति लोड हो रही है...")
        self.स्मृति = instructions
        self.IP = 0


    def fetch(self):

        if self.IP < len(self.स्मृति):

            instruction = self.स्मृति[self.IP]
            self.IP += 1

            return instruction

        return None


    def decode_execute(self, instruction):

        parts = instruction.split()

        if len(parts) == 0:
            return

        opcode = parts[0]


        # LOAD
        if opcode == "स्थापित":

            reg = parts[1]
            value = int(parts[2])

            self.रजिस्टर[reg] = value

            print(f"LOAD {reg} = {value}")


        # ADD
        elif opcode == "योग":

            reg1 = parts[1]
            reg2 = parts[2]

            self.रजिस्टर[reg1] += self.रजिस्टर[reg2]

            print(f"ADD {reg1} = {self.रजिस्टर[reg1]}")


        # SUB
        elif opcode == "घटाओ":

            reg1 = parts[1]
            reg2 = parts[2]

            self.रजिस्टर[reg1] -= self.रजिस्टर[reg2]

            print(f"SUB {reg1} = {self.रजिस्टर[reg1]}")


        # MUL
        elif opcode == "गुण":

            reg1 = parts[1]
            reg2 = parts[2]

            self.रजिस्टर[reg1] *= self.रजिस्टर[reg2]

            print(f"MUL {reg1} = {self.रजिस्टर[reg1]}")


        # DIV
        elif opcode == "भाग":

            reg1 = parts[1]
            reg2 = parts[2]

            if self.रजिस्टर[reg2] != 0:

                self.रजिस्टर[reg1] //= self.रजिस्टर[reg2]

                print(f"DIV {reg1} = {self.रजिस्टर[reg1]}")

            else:

                print("त्रुटि: division by zero")


        # SHOW
        elif opcode == "दर्शय":

            reg = parts[1]

            print(f"REGISTER {reg} = {self.रजिस्टर[reg]}")


        # JUMP
        elif opcode == "जाओ":

            address = int(parts[1])

            self.IP = address

            print(f"JUMP to {address}")


        # STOP
        elif opcode == "निर्गम":

            print("CPU STOP")

            self.सक्रिय = False


        else:

            print("अज्ञात निर्देश:", instruction)


    def चलाओ(self):

        print("CPU execution प्रारम्भ")

        self.सक्रिय = True

        while self.सक्रिय:

            instruction = self.fetch()

            if instruction is None:
                break

            self.decode_execute(instruction)

        print("CPU execution समाप्त")
