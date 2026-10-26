# 🕉️ सूत्र वास्तविक यन्त्र स्तर

class वास्तविकयन्त्र:

    def __init__(self):

        print("🕉️ सूत्र वास्तविक मशीन स्तर सक्रिय")

        # CPU Registers
        self.रजिस्टर = {
            "अ":0,
            "ब":0,
            "स":0,
            "द":0
        }

        # Instruction Map
        self.आदेशसंग्रह = {
            "LOAD": self.स्थापित,
            "ADD": self.योग,
            "SHOW": self.दर्शय,
            "END": self.समाप्त
        }

        self.चल = True


    def स्थापित(self, reg, value):

        value = int(value)

        self.रजिस्टर[reg] = value

        print(f"स्थापित: {reg} = {value}")


    def योग(self, reg1, reg2):

        result = self.रजिस्टर[reg1] + self.रजिस्टर[reg2]

        self.रजिस्टर[reg1] = result

        print(f"योग: {reg1} = {result}")


    def दर्शय(self):

        print("रजिस्टर स्थिति:")

        for k,v in self.रजिस्टर.items():

            print(f"{k} = {v}")


    def समाप्त(self):

        print("मशीन निष्पादन समाप्त")

        self.चल = False


    def निष्पादन(self, संचिका):

        print("मशीन स्तर निष्पादन प्रारम्भ")

        with open(संचिका,"r",encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            if not self.चल:
                break

            line = line.strip()

            if line == "":
                continue

            parts = line.split()

            cmd = parts[0]

            if cmd not in self.आदेशसंग्रह:

                print("अज्ञात मशीन आदेश:", cmd)

                continue

            if cmd == "LOAD":

                self.आदेशसंग्रह[cmd](parts[1], parts[2])

            elif cmd == "ADD":

                self.आदेशसंग्रह[cmd](parts[1], parts[2])

            elif cmd == "SHOW":

                self.आदेशसंग्रह[cmd]()

            elif cmd == "END":

                self.आदेशसंग्रह[cmd]()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global m
    m = वास्तविकयन्त्र()

    m.निष्पादन("test.यन्त्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
