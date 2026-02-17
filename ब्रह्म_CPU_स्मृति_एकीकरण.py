print("🕉️ ब्रह्म CPU-स्मृति एकीकरण सक्रिय")

from ब्रह्म_CPU_कर्ण import ब्रह्मCPUकर्ण
from ब्रह्म_स्मृति_कर्ण import ब्रह्मस्मृतिकर्ण


class ब्रह्मप्रणाली:

    def __init__(self):

        self.cpu = ब्रह्मCPUकर्ण()

        self.ram = ब्रह्मस्मृतिकर्ण()

        self.पते = {}


    def स्थापित(self, नाम, मान):

        पता = self.ram.आवंटन(मान)

        self.पते[नाम] = पता

        self.cpu.registers[नाम] = मान

        print("चर स्थापित:", नाम, "=", मान, "(स्मृति:", पता, ")")


    def योग(self, अ, ब):

        मान1 = self.cpu.registers.get(अ, 0)

        मान2 = self.cpu.registers.get(ब, 0)

        परिणाम = मान1 + मान2

        self.cpu.registers[अ] = परिणाम

        पता = self.पते.get(अ)

        if पता:

            self.ram.लेखन(पता, परिणाम)

        print("योग:", अ, "=", परिणाम)


    def दर्शय(self, नाम):

        मान = self.cpu.registers.get(नाम)

        print("मान:", नाम, "=", मान)


    def स्थिति(self):

        print("CPU स्थिति:")

        print(self.cpu.registers)

        self.ram.स्थिति()



if __name__ == "__main__":

    system = ब्रह्मप्रणाली()

    system.स्थापित("अ", 10)

    system.स्थापित("ब", 20)

    system.योग("अ", "ब")

    system.दर्शय("अ")

    system.स्थिति()
