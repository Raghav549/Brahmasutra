# 🕉️ सूत्र Native Executable Loader

class यन्त्रलोडक:

    def __init__(self):

        print("🕉️ सूत्र Native Executable Loader सक्रिय")

        self.रजिस्टर = {
            "अ":0,
            "ब":0,
            "स":0,
            "द":0
        }


    def निष्पादन(self, संचिका):

        print("यन्त्र लोड हो रहा है:", संचिका)

        try:

            with open(संचिका,"rb") as f:

                data = f.read()


            निर्देशसूची = data.decode("utf-8").split("\n")


            for निर्देश in निर्देशसूची:


                if निर्देश.strip()=="":
                    continue


                भाग = निर्देश.split()

                आदेश = भाग[0]


                if आदेश == "LOAD":

                    र = भाग[1]
                    मान = int(भाग[2])

                    self.रजिस्टर[र] = मान

                    print("स्थापित:", र, "=", मान)



                elif आदेश == "ADD":

                    र1 = भाग[1]
                    र2 = भाग[2]

                    self.रजिस्टर[र1] += self.रजिस्टर[र2]

                    print("योग:", र1, "=", self.रजिस्टर[र1])



                elif आदेश == "SHOW":

                    print("रजिस्टर स्थिति:")

                    for र in self.रजिस्टर:

                        print(र,"=",self.रजिस्टर[र])



                elif आदेश == "END":

                    print("निष्पादन समाप्त")

                    break



                else:

                    print("अज्ञात आदेश:", आदेश)



        except Exception as e:

            print("त्रुटि:", e)
