# 🕉️ सूत्र Executor v3


class Executor:


    def __init__(self):

        self.vars = {}

        print("🕉️ सूत्र Executor v3 सक्रिय")


    def run(self, file):

        with open(file, encoding="utf-8") as f:

            lines = f.readlines()


        pc = 0


        while pc < len(lines):

            parts = lines[pc].strip().split()

            pc += 1


            if not parts:
                continue


            cmd = parts[0]


            # variable assign
            if cmd == "संकल्प":

                var = parts[1]
                val = int(parts[2])

                self.vars[var] = val

                print(f"{var} = {val}")


            # add
            elif cmd == "योग":

                v1 = parts[1]
                v2 = parts[2]

                self.vars[v1] += self.vars[v2]

                print(f"{v1} = {self.vars[v1]}")


            # print
            elif cmd == "दर्शय":

                var = parts[1]

                print(f"{var} = {self.vars[var]}")


            # condition
            elif cmd == "यदि":

                var = parts[1]
                val = int(parts[2])

                if self.vars.get(var, 0) != val:

                    pc += 1


            # exit
            elif cmd == "निर्गम":

                print("समाप्त")

                break


            else:

                print("अज्ञात आदेश:", parts)
