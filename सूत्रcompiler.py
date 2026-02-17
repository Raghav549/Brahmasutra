# सूत्र तंत्र — Compiler
# संस्कृत source → bytecode


import json


BYTECODE_FILE = "program.sbc"


def compile_line(पंक्ति):

    पंक्ति = पंक्ति.strip()

    if पंक्ति.startswith("संकल्प"):

        भाग = पंक्ति.replace("संकल्प", "").strip()

        नाम, मान = भाग.split("=")

        return {
            "opcode": "SET",
            "name": नाम.strip(),
            "value": मान.strip()
        }

    elif पंक्ति.startswith("मुद्रय"):

        नाम = पंक्ति.replace("मुद्रय", "").strip()

        return {
            "opcode": "PRINT",
            "name": नाम
        }

    return None


def compile_file(source, output):

    bytecode = []

    with open(source, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            instr = compile_line(पंक्ति)

            if instr:
                bytecode.append(instr)

    with open(output, "w", encoding="utf-8") as f:

        json.dump(bytecode, f, ensure_ascii=False, indent=4)

    print("संकलन सफल:", output)


def परीक्षण():

    print("सूत्र Compiler सक्रिय")


if __name__ == "__main__":
    परीक्षण()
