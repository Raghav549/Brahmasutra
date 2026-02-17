# संस्कृत Compiler Engine

def compile_file(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = []

    for line in lines:

        line = line.strip()

        if line.startswith("दर्शय"):
            text = line.replace("दर्शय", "").strip()
            output.append(f'print("{text}")')

        elif line.startswith("संख्या"):
            parts = line.replace("संख्या", "").split("=")
            name = parts[0].strip()
            value = parts[1].strip()
            output.append(f"{name} = {value}")

        elif line.startswith("यदि"):
            condition = line.replace("यदि", "").strip()
            output.append(f"if {condition}:")

        elif line.startswith("अन्यथा"):
            output.append("else:")

        elif line.startswith("चक्र"):
            count = line.replace("चक्र", "").strip()
            output.append(f"for i in range({count}):")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Compilation सफल:", output_file)
