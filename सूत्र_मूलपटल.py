# 🕉️ सूत्र मूलपटल (Motherboard)

from सूत्र_CPU_RAM_एकीकरण import सूत्रCPU
from सूत्र_RAM_प्रबंधक import सूत्रRAM


class सूत्रबस:

    def __init__(self):

        print("🕉️ सूत्र बस सक्रिय")

    def भेज(self, data):

        print("बस भेज रहा है:", data)


class सूत्रभण्डारण:

    def __init__(self):

        print("🕉️ सूत्र भण्डारण सक्रिय")

    def पढ़(self, file):

        try:

            with open(file,"r",encoding="utf-8") as f:
                return f.read().splitlines()

        except:
            print("संचिका नहीं मिली")
            return None


class सूत्रमूलपटल:

    def __init__(self):

        print("🕉️ सूत्र मूलपटल सक्रिय")

        self.bus = सूत्रबस()

        self.ram = सूत्रRAM(4096)

        self.cpu = सूत्रCPU()

        self.storage = सूत्रभण्डारण()


    def कार्यक्रम_लोड(self, file):

        print("कार्यक्रम लोड हो रहा है")

        data = self.storage.पढ़(file)

        if data is None:
            return None

        addr = 0

        for line in data:

            self.ram.लिख(addr,line)

            addr += 1

        return 0


    def चलाओ(self, file):

        base = self.कार्यक्रम_लोड(file)

        if base is None:
            return

        self.cpu.pc = base

        while True:

            inst = self.ram.पढ़(self.cpu.pc)

            if inst is None:
                break

            stop = self.cpu.execute(inst)

            self.cpu.pc += 1

            if stop:
                break


# test

if __name__ == "__main__":

    board = सूत्रमूलपटल()

    board.चलाओ("test.यन्त्र")
