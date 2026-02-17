print("🕉️ ब्रह्म मशीन कर्ण सक्रिय")


class ब्रह्ममशीन:


    def __init__(self):

        self.registers = {

            0: 0,
            1: 0,
            2: 0,
            3: 0

        }

        self.pc = 0

        self.memory = []


    # LOAD PROGRAM
    def लोड(self, binary):

        print("Machine code loaded")

        self.memory = binary

        self.pc = 0


    # FETCH
    def fetch(self):

        if self.pc >= len(self.memory):

            return None

        inst = self.memory[self.pc]

        print("FETCH:", inst)

        self.pc += 1

        return inst


    # EXECUTE
    def execute(self, inst):

        opcode = inst[0]


        # LOAD
        if opcode == 1:

            reg = inst[1]

            val = inst[2]

            self.registers[reg] = val


        # ADD
        elif opcode == 2:

            r1 = inst[1]

            r2 = inst[2]

            self.registers[r1] += self.registers[r2]


        # PRINT
        elif opcode == 3:

            reg = inst[1]

            print("OUTPUT:", self.registers[reg])


    # RUN
    def run(self):

        print("Machine execution start")


        while True:

            inst = self.fetch()

            if inst is None:

                break

            self.execute(inst)

            print("REGISTERS:", self.registers)


        print("Machine execution end")
