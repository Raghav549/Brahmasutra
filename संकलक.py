# सूत्र तंत्र — संस्कृत संकलक
# Sanskrit Compiler

print("संस्कृत संकलक आरम्भ")



# opcode mapping
आदेशसङ्ख्या = {

    "संकल्प": 1,
    "दर्शय": 2,
    "योग": 3

}



# compile one line
def पंक्ति_संकलन(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:

        return None

    आदेश = शब्द[0]

    if आदेश not in आदेशसङ्ख्या:

        print("त्रुटि: अज्ञात आदेश", आदेश)

        return None

    opcode = आदेशसङ्ख्या[आदेश]

    operands = शब्द[1:]

    return (opcode, operands)



# compile file
def कार्यक्रम_संकलन(इनपुट, आउटपुट):

    bytecode = []

    with open(इनपुट, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            compiled = पंक्ति_संकलन(पंक्ति)

            if compiled:

                bytecode.append(compiled)


    with open(आउटपुट, "w", encoding="utf-8") as f:

        for opcode, operands in bytecode:

            f.write(str(opcode) + " " + " ".join(operands) + "\n")


    print("संकलन पूर्ण:", आउटपुट)



# test compile
if __name__ == "__main__":

    print("उदाहरण संकलन")

    with open("परीक्षण.sutra", "w", encoding="utf-8") as f:

        f.write("संकल्प x 5\n")
        f.write("दर्शय x\n")


    कार्यक्रम_संकलन("परीक्षण.sutra", "परीक्षण.bytecode")
