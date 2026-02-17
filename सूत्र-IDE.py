# सूत्र तंत्र — Sanskrit IDE

print("सूत्र IDE आरम्भ")



# memory
रजिस्टर = {}



# editor buffer
कोड = []



# open editor
def संपादक():

    print("संपादक आरम्भ (समाप्त करने हेतु 'समाप्त' लिखें)")


    while True:

        पंक्ति = input(">>> ")

        if पंक्ति == "समाप्त":

            break

        कोड.append(पंक्ति)



# save file
def संचय(नाम):

    with open(नाम, "w", encoding="utf-8") as f:

        for line in कोड:

            f.write(line + "\n")

    print("संचित:", नाम)



# compiler
def संकलित(नाम):

    with open(नाम, encoding="utf-8") as f:

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



# run program
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



# IDE shell
def IDE():

    while True:

        cmd = input("IDE> ")


        if cmd == "निर्गम":

            break


        elif cmd == "संपादक":

            संपादक()


        elif cmd.startswith("संचय"):

            name = cmd.split()[1]

            संचय(name)


        elif cmd.startswith("चलाओ"):

            name = cmd.split()[1]

            program = संकलित(name)

            चलाओ(program)


        else:

            print("अज्ञात आदेश")



# start IDE
if __name__ == "__main__":

    IDE()
