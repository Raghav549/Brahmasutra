class सूत्रCPU:

    def __init__(self):
        self.stack = []
        self.variables = {}

    def चलाओ(self, file):

        with open(file, "r", encoding="utf-8") as f:
            instructions = f.readlines()

        for inst in instructions:

            inst = inst.strip()

            if inst.startswith("PUSH"):
                value = inst.split()[1]
                self.stack.append(int(value))

            elif inst.startswith("POP"):
                if self.stack:
                    print(self.stack.pop())

            elif inst.startswith("SET"):
                _, name, value = inst.split()
                self.variables[name] = int(value)

            elif inst.startswith("GET"):
                _, name = inst.split()
                print(self.variables.get(name, None))

            elif inst.startswith("ADD"):
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a + b)

            elif inst.startswith("PRINT"):
                print(self.stack[-1])

        print("सूत्र execution समाप्त")
