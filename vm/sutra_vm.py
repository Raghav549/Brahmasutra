from vm.instructions import निर्देश
from vm.callstack import CallStack

class सूत्रVM:

    def __init__(self):

        self.registers = {

            "R1": 100,
            "R2": 0,
            "R3": 0,
            "R4": 0

        }

        self.instructions = निर्देश(self)

        self.labels = {}

        self.program = []

        self.pc = 0

        self.callstack = CallStack()

    def register_set(self, reg, value):

        self.registers[reg] = value

    def register_get(self, reg):

        return self.registers.get(reg, 0)

    def jump(self, label):

        if label in self.labels:

            self.pc = self.labels[label]

    def call(self, label):

        self.callstack.धकेलो(self.pc)

        self.jump(label)

    def return_(self):

        addr = self.callstack.निकालो()

        if addr is not None:

            self.pc = addr

    def bytecode_चलाओ(self, file):

        print("सूत्र VM प्रारंभ")

        with open(file, encoding="utf-8") as f:

            self.program = [line.strip() for line in f if line.strip()]

        # label scan
        for i, line in enumerate(self.program):

            parts = line.split()

            if parts[0] == "चिह्न":

                self.labels[parts[1]] = i

        self.pc = 0

        while self.pc < len(self.program):

            line = self.program[self.pc]

            parts = line.split()

            cmd = parts[0]

            args = parts[1:]

            if cmd == "आह्वान":

                self.call(args[0])

            elif cmd == "प्रत्यावर्तन":

                self.return_()

            elif hasattr(self.instructions, cmd):

                getattr(self.instructions, cmd)(*args)

            self.pc += 1

        print("सूत्र VM समाप्त")
