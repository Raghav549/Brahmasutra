# सूत्र तंत्र — Self Hosting Compiler

print("सूत्र Self Compiler आरम्भ")



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



# main
if __name__ == "__main__":

    संकलित_करो("self.sutra", "self.सूत्र")

    चलाओ("self.सूत्र")
