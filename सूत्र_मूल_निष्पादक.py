# 🕉️ सूत्र मूल यन्त्र निष्पादक


class मूलनिष्पादक:


    def __init__(self):

        self.चर = {}

        print("🕉️ सूत्र मूल निष्पादक सक्रिय")


    def चलाओ(self, संचिका):

        print(f"यन्त्र संचिका लोड: {संचिका}")


        with open(संचिका, "rb") as file:

            while True:

                डेटा = file.read(4)

                if not डेटा:

                    break


                आदेश = int.from_bytes(डेटा, "little")

                self.आदेश_चलाओ(आदेश)


        print("यन्त्र निष्पादन समाप्त")


    def आदेश_चलाओ(self, आदेश):

        if आदेश == 1:

            print("संकल्प आदेश निष्पादित")


        elif आदेश == 2:

            print("योग आदेश निष्पादित")


        elif आदेश == 3:

            print("दर्शय आदेश निष्पादित")


        elif आदेश == 0:

            print("निर्गम आदेश")

            exit()


        else:

            print("अज्ञात यन्त्र आदेश")
