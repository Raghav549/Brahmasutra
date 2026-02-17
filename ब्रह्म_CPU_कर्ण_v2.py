print("🕉️ ब्रह्म CPU कर्ण v2 सक्रिय")


class ब्रह्मCPU:


    def __init__(self):

        self.registers = {

            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0
        }

        self.memory = []

        self.pc = 0


    # FETCH
    def प्राप्त(self):

        if self.pc < len(self.memory):

            आदेश = self.memory[self.pc]

            print("FETCH:", आदेश)

            self.pc += 1

            return आदेश

        return None


    # DECODE
    def विश्लेषण(self, आदेश):

        भाग = आदेश.split()

        print("DECODE:", भाग)

        return भाग


    # EXECUTE
    def निष्पादन(self, भाग):

        आदेश = भाग[0]


        if आदेश == "स्थापित":

            self.registers[भाग[1]] = int(भाग[2])


        elif आदेश == "योग":

            self.registers[भाग[1]] += self.registers[भाग[2]]


        elif आदेश == "दर्शय":

            print("OUTPUT:", self.registers[भाग[1]])


    # WRITEBACK
    def लेखन(self):

        print("REGISTERS:", self.registers)


    # RUN
    def चलाओ(self, कार्यक्रम):

        print("CPU प्रारम्भ")

        self.memory = कार्यक्रम

        self.pc = 0


        while True:

            आदेश = self.प्राप्त()

            if आदेश is None:

                break


            भाग = self.विश्लेषण(आदेश)

            self.निष्पादन(भाग)

            self.लेखन()


        print("CPU समाप्त")
