# 🕉️ सूत्र द्विआधारी निर्माता

class द्विआधारीनिर्माता:

    def __init__(self):

        print("🕉️ सूत्र द्विआधारी निर्माता सक्रिय")

    def निर्मित(self, machine_code, filename):

        with open(filename,"wb") as f:

            for instruction in machine_code:

                # अगर instruction string है
                if isinstance(instruction,str):

                    parts = instruction.split()

                    if parts[0] == "LOAD":

                        f.write(bytes([1]))
                        f.write(bytes([int(parts[1])]))

                    elif parts[0] == "ADD":

                        f.write(bytes([2]))
                        f.write(bytes([int(parts[1])]))

                    elif parts[0] == "SHOW":

                        f.write(bytes([3]))

                    elif parts[0] == "END":

                        f.write(bytes([15]))

                # अगर instruction dict है
                elif isinstance(instruction,dict):

                    opcode = instruction["opcode"]

                    if opcode == "LOAD":

                        f.write(bytes([1]))
                        f.write(bytes([instruction["value"]]))

                    elif opcode == "ADD":

                        f.write(bytes([2]))
                        f.write(bytes([instruction["value"]]))

                    elif opcode == "SHOW":

                        f.write(bytes([3]))

                    elif opcode == "END":

                        f.write(bytes([15]))

        print("Binary निर्मित:", filename)
