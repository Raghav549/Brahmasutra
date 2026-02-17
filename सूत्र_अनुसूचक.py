# 🕉️ सूत्र अनुसूचक तंत्र


import time


class कार्य:

    def __init__(self, नाम, कार्यफल):

        self.नाम = नाम
        self.कार्यफल = कार्यफल
        self.सक्रिय = True


class सूत्रअनुसूचक:


    def __init__(self):

        self.कार्यसूची = []

        print("🕉️ सूत्र अनुसूचक सक्रिय")


    def जोड़(self, नाम, कार्यफल):

        नया = कार्य(नाम, कार्यफल)

        self.कार्यसूची.append(नया)

        print("कार्य जोड़ा:", नाम)


    def चलाओ(self):

        print("अनुसूचक प्रारम्भ")

        while True:

            सक्रिय_मिला = False

            for कार्य in self.कार्यसूची:

                if कार्य.सक्रिय:

                    सक्रिय_मिला = True

                    print("चल रहा:", कार्य.नाम)

                    कार्य.कार्यफल()

                    time.sleep(0.5)

            if not सक्रिय_मिला:

                print("कोई सक्रिय कार्य नहीं")

                break
