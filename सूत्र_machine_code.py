# 🕉️ सूत्र Machine Code Generator

class सूत्रMachineCode:

    def __init__(self):

        print("🕉️ सूत्र Machine Code Generator सक्रिय")

        self.opcodes = {

            "स्थापित": 1,
            "योग": 2,
            "घटाओ": 3,
            "गुण": 4,
            "भाग": 5,
            "दर्शय": 6,
            "निर्गम": 255

        }

        self.register_map = {

            "अ": 0,
            "ब": 1,
            "स": 2,
            "द": 3

        }


    def encode(self, program):

        machine = []

        for line in program:

            parts = line.split()

            opcode = self.opcodes.get(parts[0], 0)

            op1 = 0
            op2 = 0

            if len(parts) > 1:
                op1 = self.register_map.get(parts[1], 0)

            if len(parts) > 2:

                if parts[2].isdigit():

                    op2 = int(parts[2])

                else:

                    op2 = self.register_map.get(parts[2], 0)

            machine.append([opcode, op1, op2])

        return machine


# Compatibility alias — ``compile_run.py`` imports this name.
सूत्रMachineCodeGenerator = सूत्रMachineCode
