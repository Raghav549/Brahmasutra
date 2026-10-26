# सूत्र तंत्र — पूर्ण Computing Ecosystem




# registers
रजिस्टर = {}



# process table
प्रक्रिया = {}



# app registry
अनुप्रयोग = {}



# boot system
def boot():

    print("Boot प्रारम्भ")

    print("Kernel सक्रिय")

    print("CPU सक्रिय")

    print("Compiler सक्रिय")

    print("Shell सक्रिय")

    print("IDE सक्रिय")

    print("॥ सूत्र तंत्र तैयार ॥")



# compiler
def संकलित(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    program = []


    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue


        cmd = parts[0]


        if cmd == "संकल्प":

            program.append(("SET", parts[1], parts[2]))


        elif cmd == "योग":

            program.append(("ADD", parts[1], parts[2]))


        elif cmd == "गुण":

            program.append(("MUL", parts[1], parts[2]))


        elif cmd == "दर्शय":

            program.append(("PRINT", parts[1]))


    return program



# cpu execute
def चलाओ(program):

    for instr in program:

        cmd = instr[0]


        if cmd == "SET":

            रजिस्टर[instr[1]] = int(instr[2])

            print("SET:", instr[1], instr[2])


        elif cmd == "ADD":

            print("ADD:", रजिस्टर[instr[1]] + रजिस्टर[instr[2]])


        elif cmd == "MUL":

            print("MUL:", रजिस्टर[instr[1]] * रजिस्टर[instr[2]])


        elif cmd == "PRINT":

            print("PRINT:", रजिस्टर[instr[1]])



# install app
def अनुप्रयोग_स्थापय(नाम, file):

    अनुप्रयोग[नाम] = file

    print("अनुप्रयोग स्थापित:", नाम)



# run app
def अनुप्रयोग_चलाय(नाम):

    if नाम in अनुप्रयोग:

        program = संकलित(अनुप्रयोग[नाम])

        चलाओ(program)

    else:

        print("अनुप्रयोग नहीं मिला")



# create process
def प्रक्रिया_निर्माण(नाम):

    pid = len(प्रक्रिया) + 1

    प्रक्रिया[pid] = नाम

    print("प्रक्रिया:", pid, नाम)



# show processes
def प्रक्रिया_सूची():

    for pid in प्रक्रिया:

        print(pid, प्रक्रिया[pid])



# shell
def shell():

    while True:

        cmd = input("सूत्र> ")


        if cmd == "निर्गम":

            break


        elif cmd.startswith("स्थापय"):

            parts = cmd.split()

            अनुप्रयोग_स्थापय(parts[1], parts[2])


        elif cmd.startswith("चलाय"):

            name = cmd.split()[1]

            अनुप्रयोग_चलाय(name)


        elif cmd.startswith("प्रक्रिया"):

            name = cmd.split()[1]

            प्रक्रिया_निर्माण(name)


        elif cmd == "सूची":

            प्रक्रिया_सूची()


        else:

            print("अज्ञात आदेश")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("॥ सूत्र पूर्ण तंत्र आरम्भ ॥")
    boot()

    shell()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
