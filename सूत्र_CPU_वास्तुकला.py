# 🕉️ सूत्र CPU वास्तुकला

class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र CPU वास्तुकला सक्रिय")

        # Registers
        self.रजिस्टर = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }

        # Memory (RAM)
        self.स्मृति = [0] * 1024

        # Stack
        self.स्टैक = []

        # Instruction Pointer
        self.IP = 0

        # Program
        self.प्रोग्राम = []

        self.चल = True


    def लोड(self, संचिका):

        print("प्रोग्राम लोड:", संचिका)

        with open(संचिका,"r",encoding="utf-8") as f:

            self.प्रोग्राम = f.readlines()


    def FETCH(self):

        if self.IP >= len(self.प्रोग्राम):

            self.चल = False
            return None

        instruction = self.प्रोग्राम[self.IP].strip()

        self.IP += 1

        return instruction


    def EXECUTE(self, instruction):

        if instruction == "":
            return

        parts = instruction.split()

        cmd = parts[0]

        if cmd == "LOAD":

            reg = parts[1]
            val = int(parts[2])

            self.रजिस्टर[reg] = val

            print(f"LOAD {reg} = {val}")

        elif cmd == "ADD":

            r1 = parts[1]
            r2 = parts[2]

            result = self.रजिस्टर[r1] + self.रजिस्टर[r2]

            self.रजिस्टर[r1] = result

            print(f"ADD {r1} = {result}")

        elif cmd == "PUSH":

            reg = parts[1]

            self.स्टैक.append(self.रजिस्टर[reg])

            print(f"PUSH {reg}")

        elif cmd == "POP":

            reg = parts[1]

            self.रजिस्टर[reg] = self.स्टैक.pop()

            print(f"POP {reg}")

        elif cmd == "SHOW":

            print("Registers:")

            for k,v in self.रजिस्टर.items():

                print(k,"=",v)

        elif cmd == "END":

            print("CPU Halt")

            self.चल = False

        else:

            print("Unknown instruction:", cmd)


    def RUN(self):

        print("CPU Execution Start")

        while self.चल:

            instr = self.FETCH()

            if instr is None:
                break

            self.EXECUTE(instr)

        print("CPU Execution Complete")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cpu
    cpu = सूत्रCPU()

    cpu.लोड("test.यन्त्र")

    cpu.RUN()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
