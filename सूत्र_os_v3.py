# 🕉️ सूत्र OS v3
# पूर्ण स्वदेशी संचालन तंत्र


import सूत्र_कर्ण_v3 as कर्ण


class सूत्रOSv3:

    def __init__(self):

        print("🕉️ सूत्र OS v3 निर्माण")

        self.कर्ण = कर्ण.सूत्रकर्णv3()

        self.सक्रिय = False


    def बूट(self):

        print("🕉️ सूत्र OS बूट प्रारम्भ")

        self.कर्ण.प्रारम्भ()

        self.सक्रिय = True

        print("🕉️ सूत्र OS v3 बूट पूर्ण")


    def स्थिति(self):

        print("OS स्थिति:")

        print("सक्रिय:", self.सक्रिय)


    def चलाओ(self, नाम):

        if not self.सक्रिय:

            print("OS सक्रिय नहीं")

            return

        print("अनुप्रयोग चल रहा है:", नाम)


    def बन्द(self):

        print("OS बन्द हो रहा है")

        self.सक्रिय = False


# test

if __name__ == "__main__":

    os = सूत्रOSv3()

    os.बूट()

    os.स्थिति()

    os.चलाओ("परीक्षण")

    os.बन्द()
