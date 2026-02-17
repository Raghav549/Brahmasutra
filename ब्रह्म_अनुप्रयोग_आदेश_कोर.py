# ब्रह्म अनुप्रयोग आदेश कोर
# VERSION 28

import os

print("🕉️ ब्रह्म अनुप्रयोग आदेश कोर सक्रिय")

class ब्रह्मअनुप्रयोगआदेशकोर:

    def __init__(self):

        self.स्थापित_पथ = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_स्थापित"

        self.चल_रहे = {}

        print("🕉️ अनुप्रयोग आदेश प्रणाली तैयार")


    def अस्ति(self, नाम):

        पथ = os.path.join(self.स्थापित_पथ, नाम)

        return os.path.exists(पथ)


    def चलाओ(self, नाम):

        if not self.अस्ति(नाम):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return False

        if नाम in self.चल_रहे:

            print("सूचना: अनुप्रयोग पहले से चल रहा है")

            return True

        self.चल_रहे[नाम] = "RUNNING"

        print("अनुप्रयोग प्रारम्भ:", नाम)

        return True


    def रोकें(self, नाम):

        if नाम not in self.चल_रहे:

            print("त्रुटि: अनुप्रयोग चल नहीं रहा")

            return False

        del self.चल_रहे[नाम]

        print("अनुप्रयोग रोका गया:", नाम)

        return True


    def पुनःप्रारम्भ(self, नाम):

        print("अनुप्रयोग पुनः प्रारम्भ:", नाम)

        self.रोकें(नाम)

        self.चलाओ(नाम)

        return True


    def स्थिति(self, नाम):

        if नाम in self.चल_रहे:

            print("स्थिति: चल रहा है")

            return "RUNNING"

        print("स्थिति: बंद")

        return "STOPPED"
