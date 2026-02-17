# 🕉️ सूत्र Bytecode Generator

class BytecodeGenerator:

    def __init__(self):

        print("🕉️ सूत्र Bytecode Generator सक्रिय")

    def generate(self, ast):

        bytecode = []

        for instruction in ast:

            code = {}

            code["op"] = instruction["op"]

            if "arg1" in instruction:
                code["arg1"] = instruction["arg1"]

            if "arg2" in instruction:
                code["arg2"] = instruction["arg2"]

            bytecode.append(code)

        return bytecode


print("🕉️ सूत्र Bytecode प्रणाली तैयार")
