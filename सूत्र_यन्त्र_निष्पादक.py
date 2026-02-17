print("🕉️ सूत्र यन्त्र निष्पादक सक्रिय")

class यन्त्रनिष्पादक:

    def __init__(self):

        self.register = {}

    def निष्पादन(self, file):

        with open(file, "rb") as f:

            data = f.read()

        i = 0

        while i < len(data):

            opcode = data[i]
            i += 1

            if opcode == 1:

                var = chr(data[i])
                i += 1

                value = int.from_bytes(data[i:i+4], "big")
                i += 4

                self.register[var] = value

                print("स्थापित:", var, "=", value)

            elif opcode == 2:

                v1 = chr(data[i])
                i += 1

                v2 = chr(data[i])
                i += 1

                self.register[v1] += self.register[v2]

                print("योग:", v1, "=", self.register[v1])

            elif opcode == 3:

                var = chr(data[i])
                i += 1

                print("दर्शय:", var, "=", self.register[var])
