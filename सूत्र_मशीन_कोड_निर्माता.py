# 🕉️ सूत्र मशीन कोड निर्माता

class मशीनकोडनिर्माता:

    def __init__(self):
        self.opcodes = {
            "संकल्प": "0001",
            "योग": "0010",
            "दर्शय": "0011",
            "निर्गम": "1111"
        }

    def निर्मित(self, bytecode):

        machine_code = []

        for instruction in bytecode:

            op = instruction["op"]

            if op in self.opcodes:

                code = self.opcodes[op]

                if "arg1" in instruction:
                    code += format(hash(instruction["arg1"]) & 0xFFFF, '016b')

                if "arg2" in instruction:
                    code += format(hash(instruction["arg2"]) & 0xFFFF, '016b')

                machine_code.append(code)

        return machine_code


print("🕉️ सूत्र मशीन कोड निर्माता सक्रिय")
