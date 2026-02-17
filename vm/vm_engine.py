# सूत्र Virtual Machine

import sys

class सूत्रVM:

    def __init__(self):
        self.स्मृति = {}
        self.स्टैक = []

    def चलाओ(self, bytecode_file):

        with open(bytecode_file, "r", encoding="utf-8") as f:
            instructions = f.readlines()

        print("सूत्र VM प्रारंभ")

        for instruction in instructions:

            instruction = instruction.strip()

            if not instruction:
                continue

            parts = instruction.split("|")

            opcode = parts[0]

            if opcode == "PRINT":

                value = parts[1]

                print(value)

            else:

                print("अज्ञात आदेश:", opcode)

        print("सूत्र VM समाप्त")


def मुख्य():

    if len(sys.argv) < 2:

        print("उपयोग: सूत्र-vm file.sbc")
        return

    file = sys.argv[1]

    vm = सूत्रVM()

    vm.चलाओ(file)


if __name__ == "__main__":
    मुख्य()
