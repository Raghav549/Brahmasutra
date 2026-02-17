import os


class सूत्र_IDE:


    def __init__(self):

        self.कार्यरत = True

        print("सूत्र IDE प्रारम्भः")



    def आरम्भ(self):

        while self.कार्यरत:

            आदेश = input("सूत्र-IDE> ")

            if आदेश == "निर्गच्छ":

                self.कार्यरत = False

                print("सूत्र IDE समाप्तः")



            elif आदेश.startswith("निर्माणम्"):

                नाम = आदेश.split(" ",1)[1]

                with open(नाम,"w",encoding="utf-8") as f:

                    f.write("")

                print("सञ्चिका निर्मिता:", नाम)



            elif आदेश.startswith("लेखनम्"):

                भाग = आदेश.split(" ",2)

                नाम = भाग[1]

                विषय = भाग[2]

                with open(नाम,"w",encoding="utf-8") as f:

                    f.write(विषय)

                print("लेखनं सम्पन्नम्")



            elif आदेश.startswith("पठनम्"):

                नाम = आदेश.split(" ",1)[1]

                if os.path.exists(नाम):

                    with open(नाम,"r",encoding="utf-8") as f:

                        print(f.read())

                else:

                    print("सञ्चिका नास्ति")



            elif आदेश.startswith("चलनम्"):

                नाम = आदेश.split(" ",1)[1]

                if os.path.exists(नाम):

                    with open(नाम,"r",encoding="utf-8") as f:

                        कोड = f.read()

                        exec(कोड)

                else:

                    print("सञ्चिका नास्ति")



            elif आदेश == "सूची":

                सञ्चिकाः = os.listdir()

                for स in सञ्चिकाः:

                    print(स)



            else:

                print("अज्ञात आदेश")
