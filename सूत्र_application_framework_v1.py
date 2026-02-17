# 🕉️ सूत्र Application Framework v1
# पूर्ण स्वदेशी अनुप्रयोग ढाँचा


import सूत्र_os_v3 as os_v3


class सूत्रअनुप्रयोग:

    def __init__(self, नाम):

        self.नाम = नाम

        self.स्थिति = "बन्द"

        print("अनुप्रयोग निर्मित:", नाम)


    def प्रारम्भ(self):

        self.स्थिति = "सक्रिय"

        print("अनुप्रयोग सक्रिय:", self.नाम)


    def बन्द(self):

        self.स्थिति = "बन्द"

        print("अनुप्रयोग बन्द:", self.नाम)



class सूत्रApplicationFramework:

    def __init__(self):

        print("🕉️ सूत्र Application Framework निर्माण")

        self.os = os_v3.सूत्रOSv3()

        self.os.बूट()

        self.अनुप्रयोगसूची = {}

        self.सक्रिय = True


    def प्रारम्भ(self):

        print("🕉️ Application Framework सक्रिय")

        while self.सक्रिय:

            self.मेनू()

            आदेश = input("App >>> ")

            self.निष्पादन(आदेश)


    def मेनू(self):

        print("")
        print("====== सूत्र Application Framework ======")

        print("१. अनुप्रयोग register")

        print("२. अनुप्रयोग start")

        print("३. अनुप्रयोग stop")

        print("४. अनुप्रयोग list")

        print("५. निर्गम")

        print("========================================")


    def निष्पादन(self, आदेश):

        if आदेश == "१":

            नाम = input("अनुप्रयोग नाम: ")

            self.register(नाम)


        elif आदेश == "२":

            नाम = input("अनुप्रयोग नाम: ")

            self.start(नाम)


        elif आदेश == "३":

            नाम = input("अनुप्रयोग नाम: ")

            self.stop(नाम)


        elif आदेश == "४":

            self.list()


        elif आदेश == "५":

            print("Framework बन्द")

            self.os.बन्द()

            self.सक्रिय = False


        else:

            print("अमान्य आदेश")


    def register(self, नाम):

        app = सूत्रअनुप्रयोग(नाम)

        self.अनुप्रयोगसूची[नाम] = app


    def start(self, नाम):

        if नाम in self.अनुप्रयोगसूची:

            self.अनुप्रयोगसूची[नाम].प्रारम्भ()

        else:

            print("अनुप्रयोग नहीं मिला")


    def stop(self, नाम):

        if नाम in self.अनुप्रयोगसूची:

            self.अनुप्रयोगसूची[नाम].बन्द()

        else:

            print("अनुप्रयोग नहीं मिला")


    def list(self):

        print("अनुप्रयोग सूची:")

        for नाम, app in self.अनुप्रयोगसूची.items():

            print(नाम, "-", app.स्थिति)



# start framework

if __name__ == "__main__":

    framework = सूत्रApplicationFramework()

    framework.प्रारम्भ()
