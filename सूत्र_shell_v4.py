# 🕉️ सूत्र Shell v4
# पूर्ण स्वदेशी OS shell


import सूत्र_os_v3 as os_v3


class सूत्रShellv4:

    def __init__(self):

        print("🕉️ सूत्र Shell v4 निर्माण")

        self.os = os_v3.सूत्रOSv3()

        self.os.बूट()

        self.सक्रिय = True


    def प्रारम्भ(self):

        print("🕉️ सूत्र Shell v4 सक्रिय")
        print("निर्गम लिखकर बन्द करें")


        while self.सक्रिय:

            आदेश = input("सूत्र >>> ")

            self.आदेश_निष्पादन(आदेश)


    def आदेश_निष्पादन(self, आदेश):

        भाग = आदेश.strip().split()

        if len(भाग) == 0:
            return


        cmd = भाग[0]


        if cmd == "निर्गम":

            print("Shell बन्द")
            self.सक्रिय = False
            self.os.बन्द()


        elif cmd == "स्थिति":

            self.os.स्थिति()


        elif cmd == "चलाओ":

            if len(भाग) < 2:

                print("नाम दें")

                return

            self.os.चलाओ(भाग[1])


        elif cmd == "सहायता":

            print("उपलब्ध आदेश:")
            print("स्थिति")
            print("चलाओ नाम")
            print("निर्गम")


        else:

            print("अज्ञात आदेश:", आदेश)



# start shell

if __name__ == "__main__":

    shell = सूत्रShellv4()

    shell.प्रारम्भ()
