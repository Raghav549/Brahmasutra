# 🕉️ सूत्र Executor v5 (Function support)


class Executor:


    def __init__(self):

        self.vars = {}
        self.functions = {}
        self.loop_stack = []

        print("🕉️ सूत्र Executor v5 सक्रिय")


    def load_functions(self, lines):

        pc = 0

        while pc < len(lines):

            parts = lines[pc].strip().split()

            if parts and parts[0] == "क्रिया":

                fname = parts[1]
                start = pc + 1

                while lines[pc].strip() != "समाप्त":

                    pc += 1

                end = pc

                self.functions[fname] = (start, end)

            pc += 1


    def run(self, file):

        with open(file, encoding="utf-8") as f:

            lines = f.readlines()


        self.load_functions(lines)

        pc = 0


        while pc < len(lines):

            parts = lines[pc].strip().split()

            if not parts:

                pc += 1
                continue


            cmd = parts[0]


            # skip function definition
            if cmd == "क्रिया":

                while lines[pc].strip() != "समाप्त":

                    pc += 1

                pc += 1
                continue


            # assign
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


            # function call
            elif cmd == "आह्वान":

                fname = parts[1]

                if fname in self.functions:

                    start, end = self.functions[fname]

                    for i in range(start, end):

                        fparts = lines[i].strip().split()

                        if fparts and fparts[0] == "दर्शय":

                            var = fparts[1]
                            print(f"{var} = {self.vars[var]}")

                pc += 1


            # exit
            elif cmd == "निर्गम":

                print("समाप्त")
                break


            else:

                pc += 1
