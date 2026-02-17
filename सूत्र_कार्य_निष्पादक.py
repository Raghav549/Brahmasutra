import os

class कार्यनिष्पादक:

    def __init__(self):

        print("🕉️ सूत्र कार्य निष्पादक सक्रिय")

        self.registers = {}


    def parse_line(self, line):

        line = line.strip()

        if line == "":

            return None

        if line.startswith("सूत्रयन्त्र"):

            return None

        parts = line.split()

        return parts


    def निष्पादन(self, path):

        print("कार्य लोड:", path)

        if not os.path.exists(path):

            print("त्रुटि: कार्य नहीं मिला")

            return


        with open(path, "r", encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            cmd = self.parse_line(line)

            if not cmd:

                continue


            if cmd[0] == "स्थापित":

                var = cmd[1]

                val = int(cmd[2])

                self.registers[var] = val

                print(f"स्थापित: {var} = {val}")


            elif cmd[0] == "योग":

                var1 = cmd[1]

                var2 = cmd[2]

                result = self.registers.get(var1,0) + self.registers.get(var2,0)

                self.registers[var1] = result

                print(f"योग: {var1} = {result}")


            elif cmd[0] == "दर्शय":

                var = cmd[1]

                print(f"दर्शय: {var} = {self.registers.get(var,0)}")


            else:

                print("त्रुटि: अमान्य कार्य", line.strip())
