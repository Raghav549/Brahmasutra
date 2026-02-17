# सूत्र Native Compiler

MAGIC = "SUTRA_BIN_V1"

def compile_native(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:

        bytecode = f.read()

    with open(output_file, "w", encoding="utf-8") as f:

        f.write(MAGIC + "\n")

        f.write(bytecode)

    print("Native binary निर्मित:")
    print(output_file)
