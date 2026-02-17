# 🕉️ सूत्र Parser

class Parser:

    def __init__(self):
        print("🕉️ सूत्र Parser सक्रिय")

    def parse_file(self, filename):

        ast = []

        with open(filename,"r",encoding="utf-8") as f:

            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            parts = line.split()

            instruction = {}

            instruction["op"] = parts[0]

            if len(parts) > 1:
                instruction["arg1"] = parts[1]

            if len(parts) > 2:
                instruction["arg2"] = parts[2]

            ast.append(instruction)

        return ast


print("🕉️ सूत्र Parser तैयार")
