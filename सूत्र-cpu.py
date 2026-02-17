# सूत्र तंत्र — Sanskrit CPU and VM

print("सूत्र CPU आरम्भ")



# registers
रजिस्टर = {
    "अ": 0,
    "ब": 0,
    "स": 0,
    "द": 0
}



# instruction execution
def निर्देश_चलाओ(निर्देश):

    शब्द = निर्देश.strip().split()

    if len(शब्द) == 0:
        return


    आदेश = शब्द[0]


    # load
    if आदेश == "लोड":

        रजिस्टर[शब्द[1]] = int(शब्द[2])

        print("लोड:", शब्द[1], "=", शब्द[2])


    # add
    elif आदेश == "योग":

        रजिस्टर[शब्द[1]] += रजिस्टर[शब्द[2]]

        print("योग:", रजिस्टर[शब्द[1]])


    # multiply
    elif आदेश == "गुण":

        रजिस्टर[शब्द[1]] *= रजिस्टर[शब्द[2]]

        print("गुण:", रजिस्टर[शब्द[1]])


    # print
    elif आदेश == "दर्शय":

        print("मान:", रजिस्टर[शब्द[1]])



# run program
def कार्यक्रम_चलाओ(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    for line in lines:

        निर्देश_चलाओ(line)



# start
if __name__ == "__main__":

    कार्यक्रम_चलाओ("cpu.sutra")
