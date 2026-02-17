print("🕉️ ब्रह्म CPU कर्ण सक्रिय")


class ब्रह्मCPUकर्ण:

    def __init__(self):

        # CPU registers
        self.registers = {

            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0

        }

        self.program_counter = 0


    def स्थापित(self, नाम, मान):

        self.registers[नाम] = मान

        print("CPU स्थापित:", नाम, "=", मान)


    def प्राप्त(self, नाम):

        return self.registers.get(नाम, 0)


    def योग(self, अ, ब):

        परिणाम = self.registers.get(अ, 0) + self.registers.get(ब, 0)

        self.registers[अ] = परिणाम

        print("CPU योग:", अ, "=", परिणाम)


    def स्थिति(self):

        print("CPU Registers:")

        for k, v in self.registers.items():

            print(k, "=", v)
