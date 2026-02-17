# 🕉️ सूत्र Machine Code Generator

class MachineCodeGenerator:

    def __init__(self):

        print("🕉️ सूत्र Machine Code Generator सक्रिय")

    def generate(self, bytecode):

        machine = []

        for instruction in bytecode:

            if instruction["type"] == "LOAD":

                machine.append({
                    "opcode":"LOAD",
                    "value":instruction["value"]
                })

            elif instruction["type"] == "ADD":

                machine.append({
                    "opcode":"ADD",
                    "value":instruction["value"]
                })

            elif instruction["type"] == "SHOW":

                machine.append({
                    "opcode":"SHOW"
                })

        machine.append({
            "opcode":"END"
        })

        return machine
