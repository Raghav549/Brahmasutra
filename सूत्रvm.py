# सूत्र तंत्र — Virtual Machine
# Bytecode Execution Engine

import json


class सूत्रVM:

    def __init__(self):
        self.memory = {}

    def run(self, bytecode_file):

        with open(bytecode_file, "r", encoding="utf-8") as f:
            program = json.load(f)

        for instruction in program:

            opcode = instruction["opcode"]

            if opcode == "SET":

                name = instruction["name"]
                value = instruction["value"]

                self.memory[name] = value

            elif opcode == "PRINT":

                name = instruction["name"]

                if name in self.memory:
                    print("फल:", self.memory[name])
                else:
                    print("त्रुटि: अपरिभाषित", name)


def परीक्षण():

    print("सूत्र VM सक्रिय")


if __name__ == "__main__":
    परीक्षण()
