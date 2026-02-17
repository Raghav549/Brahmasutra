# 🕉️ सूत्र Machine Code CPU Executor

class सूत्रMachineCPU:

    def __init__(self):

        print("🕉️ सूत्र Machine CPU सक्रिय")

        self.registers = {

            0: 0,
            1: 0,
            2: 0,
            3: 0

        }

        self.running = True


    def run(self, machine_code):

        ip = 0

        while self.running and ip < len(machine_code):

            instruction = machine_code[ip]

            opcode = instruction[0]
            op1 = instruction[1]
            op2 = instruction[2]


            # स्थापित
            if opcode == 1:

                self.registers[op1] = op2


            # योग
            elif opcode == 2:

                self.registers[op1] += self.registers[op2]


            # घटाओ
            elif opcode == 3:

                self.registers[op1] -= self.registers[op2]


            # गुण
            elif opcode == 4:

                self.registers[op1] *= self.registers[op2]


            # भाग
            elif opcode == 5:

                if self.registers[op2] != 0:

                    self.registers[op1] //= self.registers[op2]


            # दर्शय
            elif opcode == 6:

                print("REGISTER VALUE:", self.registers[op1])


            # निर्गम
            elif opcode == 255:

                print("PROGRAM END")
                self.running = False


            ip += 1
