
class द्विआधारीनिष्पादक:

    def __init__(self):
        print("🕉️ सूत्र CPU निष्पादक सक्रिय")

        self.registers = {
            "अ": 0,
            "ब": 0,
            "स": 0,
            "द": 0
        }

        self.opcodes = {
            1: "LOAD",
            2: "ADD",
            3: "SHOW",
            4: "END"
        }

    def निष्पादन(self, संचिका):

        print("Binary लोड:", संचिका)

        with open(संचिका, "rb") as f:
            data = f.read()

        i = 0

        while i < len(data):

            opcode = data[i]
            i += 1

            if opcode == 1:

                reg = data[i]
                i += 1

                value = int.from_bytes(data[i:i+4], "big")
                i += 4

                reg_name = chr(reg)

                self.registers[reg_name] = value

                print("LOAD", reg_name, "=", value)


            elif opcode == 2:

                reg1 = chr(data[i])
                reg2 = chr(data[i+1])
                i += 2

                self.registers[reg1] += self.registers[reg2]

                print("ADD result =", self.registers[reg1])


            elif opcode == 3:

                reg = chr(data[i])
                i += 1

                print("REGISTER", reg, "=", self.registers[reg])


            elif opcode == 4:

                print("PROGRAM END")
                break


            else:

                print("Unknown opcode:", opcode)
                break


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ सूत्र द्विआधारी निष्पादक तैयार")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
