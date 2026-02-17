# 🕉️ सूत्र CPU-RAM एकीकरण

from सूत्र_RAM_प्रबंधक import सूत्रRAM


class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र CPU सक्रिय")

        self.register = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }

        self.pc = 0


    def execute(self, instruction):

        parts = instruction.split()

        if len(parts) == 0:
            return False

        opcode = parts[0]

        if opcode == "LOAD":

            reg = parts[1]
            val = int(parts[2])

            self.register[reg] = val

            print(f"LOAD → {reg} = {val}")


        elif opcode == "ADD":

            r1 = parts[1]
            r2 = parts[2]

            self.register[r1] += self.register[r2]

            print(f"ADD → {r1} = {self.register[r1]}")


        elif opcode == "SHOW":

            print("REGISTER स्थिति:")

            for r,v in self.register.items():
                print(r,"=",v)


        elif opcode == "END":

            print("Program समाप्त")

            return True


        else:

            print("अज्ञात आदेश:",opcode)

        return False


class सूत्रप्रणाली:

    def __init__(self):

        print("🕉️ सूत्र CPU-RAM प्रणाली सक्रिय")

        self.ram = सूत्रRAM(2048)

        self.cpu = सूत्रCPU()


    def run(self, file):

        base = self.ram.कार्यक्रम_लोड(file)

        if base is None:
            return

        self.cpu.pc = base

        while True:

            instruction = self.ram.पढ़(self.cpu.pc)

            if instruction is None:
                break

            stop = self.cpu.execute(instruction)

            self.cpu.pc += 1

            if stop:
                break


# test

if __name__ == "__main__":

    system = सूत्रप्रणाली()

    system.run("test.यन्त्र")
