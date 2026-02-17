# 🕉️ सूत्र Executor v4


class Executor:


    def __init__(self):

        self.vars = {}
        self.loop_stack = []

        print("🕉️ सूत्र Executor v4 सक्रिय")


    def run(self, file):

        with open(file, encoding="utf-8") as f:

            lines = f.readlines()


        pc = 0


        while pc < len(lines):

            parts = lines[pc].strip().split()

            if not parts:

                pc += 1
                continue


            cmd = parts[0]


            # variable assign
            if cmd == "संकल्प":

                var = parts[1]
                val = int(parts[2])

                self.vars[var] = val

                print(f"{var} = {val}")

                pc += 1


            # add
            elif cmd == "योग":

                v1 = parts[1]
                v2 = parts[2]

                if v2.isdigit():

                    self.vars[v1] += int(v2)

                else:

                    self.vars[v1] += self.vars[v2]

                pc += 1


            # print
            elif cmd == "दर्शय":

                var = parts[1]

                print(f"{var} = {self.vars[var]}")

                pc += 1


            # loop start
            elif cmd == "यावत्":

                var = parts[1]
                val = int(parts[2])

                if self.vars.get(var, 0) <= val:

                    self.loop_stack.append((pc, var, val))
                    pc += 1

                else:

                    # skip loop
                    while lines[pc].strip() != "समाप्त":

                        pc += 1

                    pc += 1


            # loop end
            elif cmd == "समाप्त":

                if self.loop_stack:

                    loop_start, var, val = self.loop_stack[-1]

                    if self.vars.get(var, 0) <= val:

                        pc = loop_start

                    else:

                        self.loop_stack.pop()
                        pc += 1

                else:

                    pc += 1


            # exit
            elif cmd == "निर्गम":

                print("समाप्त")
                break


            else:

                print("अज्ञात आदेश:", parts)
                pc += 1
