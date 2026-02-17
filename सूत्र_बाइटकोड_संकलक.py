print("🕉️ सूत्र बाइटकोड संकलक सक्रिय")

class बाइटकोडसंकलक:

    def __init__(self):
        self.opcodes = {
            "संकल्प": 1,
            "योग": 2,
            "दर्शय": 3
        }

    def संकलन(self, input_file, output_file):

        bytecode = []

        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            cmd = parts[0]

            if cmd not in self.opcodes:
                print("अमान्य आदेश:", cmd)
                continue

            opcode = self.opcodes[cmd]

            instruction = [opcode]

            for p in parts[1:]:
                instruction.append(p)

            bytecode.append(instruction)

        with open(output_file, "w", encoding="utf-8") as f:

            for instr in bytecode:

                f.write(" ".join(map(str, instr)) + "\n")

        print("संकलन पूर्ण:", output_file)
