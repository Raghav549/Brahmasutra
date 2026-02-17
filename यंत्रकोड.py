# सूत्र तंत्र — यंत्रकोड स्तर
# Sanskrit Machine Code Engine

print("यंत्रकोड स्तर आरम्भ")



# registers
पञ्जिका = {

    "अ": 0,
    "ब": 0,
    "स": 0,
    "द": 0

}



# memory
स्मृति = [0] * 256



# instruction execution
def आदेश_चलाओ(आदेश):

    भाग = आदेश.split()

    if len(भाग) == 0:

        return


    नाम = भाग[0]


    # LOAD
    if नाम == "भार":

        र = भाग[1]

        मान = int(भाग[2])

        पञ्जिका[र] = मान

        print("भार:", र, मान)


    # ADD
    elif नाम == "योग":

        र1 = भाग[1]

        र2 = भाग[2]

        पञ्जिका[र1] += पञ्जिका[र2]

        print("योग:", पञ्जिका[र1])


    # STORE
    elif नाम == "संग्रह":

        र = भाग[1]

        स्थान = int(भाग[2])

        स्मृति[स्थान] = पञ्जिका[र]

        print("संग्रह:", स्थान, स्मृति[स्थान])


    # PRINT
    elif नाम == "दर्शय":

        र = भाग[1]

        print("मान:", पञ्जिका[र])


    else:

        print("अज्ञात आदेश:", आदेश)



# run machine code file
def कार्यक्रम_चलाओ(फाइल):

    with open(फाइल, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            आदेश_चलाओ(पंक्ति.strip())



# test machine code
if __name__ == "__main__":

    with open("यंत्र.smc", "w", encoding="utf-8") as f:

        f.write("भार अ 5\n")
        f.write("भार ब 10\n")
        f.write("योग अ ब\n")
        f.write("दर्शय अ\n")


    कार्यक्रम_चलाओ("यंत्र.smc")
