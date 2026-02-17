print("🕉️ सूत्र बाइटकोड निष्पादक सक्रिय")

class बाइटकोडनिष्पादक:

    def __init__(self):

        self.memory = {}

    def निष्पादन(self, file):

        with open(file, "r", encoding="utf-8") as f:

            lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue

            opcode = int(parts[0])

            if opcode == 1:

                var = parts[1]
                value = int(parts[2])

                self.memory[var] = value

                print("स्थापित:", var, "=", value)

            elif opcode == 2:

                v1 = parts[1]
                v2 = parts[2]

                result = self.memory.get(v1, 0) + self.memory.get(v2, 0)

                self.memory[v1] = result

                print("योग:", v1, "=", result)

            elif opcode == 3:

                var = parts[1]

                print("दर्शय:", var, "=", self.memory.get(var, 0))

            else:

                print("अज्ञात opcode:", opcode)
