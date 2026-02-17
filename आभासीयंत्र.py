# सूत्र तंत्र — संस्कृत आभासी यंत्र
# Sanskrit Virtual Machine

print("संस्कृत आभासी यंत्र आरम्भ")



# variable storage
चर = {}



# execute bytecode instruction
def आदेश_चलाओ(opcode, operands):

    opcode = int(opcode)


    # संकल्प
    if opcode == 1:

        नाम = operands[0]

        मान = int(operands[1])

        चर[नाम] = मान

        print("चर निर्मित:", नाम)


    # दर्शय
    elif opcode == 2:

        नाम = operands[0]

        if नाम in चर:

            print("मान:", चर[नाम])

        else:

            print("अज्ञात चर:", नाम)


    # योग
    elif opcode == 3:

        अ = operands[0]

        ब = operands[1]

        परिणाम = चर.get(अ, 0) + चर.get(ब, 0)

        print("योग:", परिणाम)


    else:

        print("अज्ञात opcode:", opcode)



# run bytecode file
def कार्यक्रम_चलाओ(फाइल):

    with open(फाइल, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            भाग = पंक्ति.strip().split()

            opcode = भाग[0]

            operands = भाग[1:]

            आदेश_चलाओ(opcode, operands)



# test run
if __name__ == "__main__":

    कार्यक्रम_चलाओ("परीक्षण.bytecode")
