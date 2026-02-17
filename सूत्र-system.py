# सूत्र तंत्र — पूर्ण Sanskrit Operating System

print("सूत्र तंत्र आरम्भ")



# memory
स्मृति = {}



# registers
रजिस्टर = {
    "अ": 0,
    "ब": 0,
    "स": 0
}



# process list
प्रक्रिया = []



# boot
def boot():

    print("Boot प्रारम्भ...")

    print("Kernel लोड...")

    print("Compiler लोड...")

    print("CPU लोड...")

    print("Shell लोड...")

    print("सूत्र तंत्र तैयार")



# compiler
def संकलित(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    output = []

    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue


        cmd = parts[0]


        if cmd == "संकल्प":

            output.append(("SET", parts[1], parts[2]))


        elif cmd == "योग":

            output.append(("ADD", parts[1], parts[2]))


        elif cmd == "गुण":

            output.append(("MUL", parts[1], parts[2]))


        elif cmd == "दर्शय":

            output.append(("PRINT", parts[1]))


    return output



# CPU execute
def चलाओ(program):

    for instr in program:

        cmd = instr[0]


        if cmd == "SET":

            रजिस्टर[instr[1]] = int(instr[2])

            print("SET:", instr[1], instr[2])


        elif cmd == "ADD":

            result = रजिस्टर[instr[1]] + रजिस्टर[instr[2]]

            print("ADD:", result)


        elif cmd == "MUL":

            result = रजिस्टर[instr[1]] * रजिस्टर[instr[2]]

            print("MUL:", result)


        elif cmd == "PRINT":

            print("PRINT:", रजिस्टर[instr[1]])



# shell
def shell():

    while True:

        cmd = input("सूत्र> ")


        if cmd == "निर्गम":

            print("System बंद")

            break


        elif cmd.startswith("चलाओ"):

            file = cmd.split()[1]

            program = संकलित(file)

            चलाओ(program)


        elif cmd.startswith("प्रक्रिया"):

            name = cmd.split()[1]

            प्रक्रिया.append(name)

            print("प्रक्रिया आरम्भ:", name)


        elif cmd == "सूची":

            print("प्रक्रियाएँ:")

            for p in प्रक्रिया:

                print(p)


        else:

            print("अज्ञात आदेश")



# start system
if __name__ == "__main__":

    boot()

    shell()
