# सूत्र तंत्र — पूर्ण संस्कृत दुभाषिया
# Full Sanskrit Interpreter

print("संस्कृत दुभाषिया आरम्भ")



# variable storage
चर = {}



# execute one line
def पंक्ति_चलाओ(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:
        return


    # print
    if शब्द[0] == "दर्शय":

        नाम = शब्द[1]

        if नाम in चर:

            print(चर[नाम])

        else:

            print(नाम)



    # assignment
    elif शब्द[0] == "संकल्प":

        नाम = शब्द[1]

        मान = int(शब्द[2])

        चर[नाम] = मान

        print("चर बना:", नाम)



    # addition
    elif शब्द[0] == "योग":

        अ = चर.get(शब्द[1], 0)

        ब = चर.get(शब्द[2], 0)

        परिणाम = अ + ब

        print("योग:", परिणाम)



    else:

        print("अज्ञात आदेश:", पंक्ति)



# run program
def कार्यक्रम_चलाओ(फाइल):

    with open(फाइल, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            पंक्ति_चलाओ(पंक्ति)



# interactive mode
def संवाद():

    print("संवाद मोड सक्रिय")

    while True:

        पंक्ति = input("सूत्र >>> ")

        if पंक्ति == "निर्गम":

            break

        पंक्ति_चलाओ(पंक्ति)



# start interactive
संवाद()
