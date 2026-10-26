# सूत्र तंत्र — Self Hosting Compiler




# memory
चर = {}



# compile Sanskrit source into executable
def संकलित_करो(स्रोत, लक्ष्य):

    with open(स्रोत, encoding="utf-8") as f:

        lines = f.readlines()


    output = []

    output.append("सूत्रEXEC")


    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue


        आदेश = parts[0]


        if आदेश == "संकल्प":

            output.append("SET " + parts[1] + " " + parts[2])


        elif आदेश == "योग":

            output.append("ADD " + parts[1] + " " + parts[2])


        elif आदेश == "गुण":

            output.append("MUL " + parts[1] + " " + parts[2])


        elif आदेश == "दर्शय":

            output.append("PRINT " + parts[1])


    with open(लक्ष्य, "w", encoding="utf-8") as f:

        for line in output:

            f.write(line + "\n")


    print("Self compilation पूर्ण:", लक्ष्य)



# execute executable
def चलाओ(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    reg = {}


    for line in lines[1:]:

        parts = line.strip().split()

        cmd = parts[0]


        if cmd == "SET":

            reg[parts[1]] = int(parts[2])

            print("SET:", parts[1], reg[parts[1]])


        elif cmd == "ADD":

            result = reg[parts[1]] + reg[parts[2]]

            print("ADD:", result)


        elif cmd == "MUL":

            result = reg[parts[1]] * reg[parts[2]]

            print("MUL:", result)


        elif cmd == "PRINT":

            print("PRINT:", reg[parts[1]])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Self Compiler आरम्भ")
    संकलित_करो("self.sutra", "self.सूत्र")

    चलाओ("self.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
