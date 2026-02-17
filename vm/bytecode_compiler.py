# सूत्र Bytecode Compiler

OPCODES = {
    "पाठ": "PRINT",
    "चर": "STORE",
    "यदि": "IF",
    "चक्र": "LOOP"
}


def compile_to_bytecode(input_file, output_file):

    bytecode = []

    with open(input_file, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        parts = line.split(" ", 1)

        instruction = parts[0]

        argument = ""

        if len(parts) > 1:
            argument = parts[1]

        if instruction in OPCODES:

            opcode = OPCODES[instruction]

            bytecode.append(f"{opcode}|{argument}")


    with open(output_file, "w", encoding="utf-8") as f:

        for code in bytecode:
            f.write(code + "\n")


    print("Bytecode निर्मित:")
    print(output_file)
