# =========================================
# सूत्र तंत्र — संस्कृत सञ्चिका प्रणाली
# =========================================

import os

print("🕉️ सूत्र सञ्चिका प्रणाली सक्रिय")
print("लिखत: सहायता")


मूल = "सूत्र-सञ्चिका"

# root folder create
if not os.path.exists(मूल):
    os.mkdir(मूल)


def मार्ग(नाम):

    return os.path.join(मूल, नाम)



while True:

    आदेश = input("सञ्चिका >>> ")

    भाग = आदेश.split()

    if len(भाग) == 0:
        continue


    # निर्गम

    if भाग[0] == "निर्गम":

        print("सञ्चिका प्रणाली समाप्त")
        break


    # सहायता

    elif भाग[0] == "सहायता":

        print("आदेश:")
        print("निर्माण नाम")
        print("लेख नाम पाठ")
        print("पठ नाम")
        print("सूची")
        print("विलोप नाम")
        print("निर्गम")


    # create file

    elif भाग[0] == "निर्माण":

        नाम = मार्ग(भाग[1])

        open(नाम, "w").close()

        print("सञ्चिका निर्मित:", भाग[1])



    # write file

    elif भाग[0] == "लेख":

        नाम = मार्ग(भाग[1])

        पाठ = " ".join(भाग[2:])

        with open(नाम, "w", encoding="utf-8") as f:
            f.write(पाठ)

        print("लेखन सफल")



    # read file

    elif भाग[0] == "पठ":

        नाम = मार्ग(भाग[1])

        if os.path.exists(नाम):

            with open(नाम, "r", encoding="utf-8") as f:

                print("पाठ:", f.read())

        else:

            print("त्रुटि: सञ्चिका नहीं")


    # list files

    elif भाग[0] == "सूची":

        files = os.listdir(मूल)

        print("सञ्चिकाएँ:")

        for f in files:
            print("-", f)



    # delete file

    elif भाग[0] == "विलोप":

        नाम = मार्ग(भाग[1])

        if os.path.exists(नाम):

            os.remove(नाम)

            print("विलोप सफल")

        else:

            print("सञ्चिका नहीं")


    else:

        print("अज्ञात आदेश")
