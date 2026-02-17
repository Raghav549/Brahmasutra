# 🕉️ सूत्र वास्तविक हार्डवेयर मशीन

from सूत्र_वास्तविक_CPU import सूत्रCPU
from सूत्र_स्मृति_RAM import सूत्रRAM
from सूत्र_BUS import सूत्रBUS


class सूत्रHardwareMachine:

    def __init__(self):

        print("🕉️ सूत्र हार्डवेयर मशीन निर्माण")

        self.cpu = सूत्रCPU()

        self.ram = सूत्रRAM()

        self.bus = सूत्रBUS()


    def program_load(self, program):

        print("प्रोग्राम RAM में लोड हो रहा है")

        address = 0

        for instruction in program:

            self.ram.लिखो(address, instruction)

            address += 1


    def execute(self):

        print("हार्डवेयर निष्पादन प्रारम्भ")

        address = 0

        program = []

        while True:

            instruction = self.ram.memory.get(address,None)

            if instruction is None:

                break

            program.append(instruction)

            address += 1


        self.cpu.EXECUTE(program)


    def status(self):

        print("हार्डवेयर स्थिति")

        self.ram.स्थिति()

        self.cpu.STATE()
