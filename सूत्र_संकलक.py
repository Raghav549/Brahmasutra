# 🕉️ सूत्र संकलक (Compiler)

class संकलक:


    OPCODES = {

        "संकल्प": 1,
        "योग": 2,
        "दर्शय": 3,
        "निर्गम": 4

    }


    REGISTERS = {

        "अ": 1,
        "ब": 2,
        "स": 3,
        "द": 4

    }


    def संकलित(self, input_file, output_file):

        bytecode = []


        with open(input_file, encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue


            cmd = parts[0]


            if cmd == "संकल्प":

                bytecode.append(self.OPCODES[cmd])
                bytecode.append(self.REGISTERS[parts[1]])
                bytecode.append(int(parts[2]))


            elif cmd == "योग":

                bytecode.append(self.OPCODES[cmd])
                bytecode.append(self.REGISTERS[parts[1]])
                bytecode.append(self.REGISTERS[parts[2]])


            elif cmd == "दर्शय":

                bytecode.append(self.OPCODES[cmd])
                bytecode.append(self.REGISTERS[parts[1]])


            elif cmd == "निर्गम":

                bytecode.append(self.OPCODES[cmd])


        with open(output_file, "wb") as f:

            f.write(bytes(bytecode))


        print("🕉️ संकलन सफल:", output_file)


# ---------------------------------------------------------------------------
# अनुकूलता (compatibility) — पुराने डेमो `सूत्रसंकलक` नाम और `संकलन` विधि
# का उपयोग करते हैं। ये aliases उन्हें बिना बदले चलने देते हैं।
# ---------------------------------------------------------------------------
सूत्रसंकलक = संकलक

if not hasattr(संकलक, "संकलन"):
    संकलक.संकलन = संकलक.संकलित
