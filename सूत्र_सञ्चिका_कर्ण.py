# 🕉️ सूत्र सञ्चिका कर्ण तंत्र


import os


class सूत्रसञ्चिकाकर्ण:


    def __init__(self):

        self.मूलपथ = os.path.expanduser("~/सूत्र-तंत्र/संग्रह")

        os.makedirs(self.मूलपथ, exist_ok=True)

        print("🕉️ सञ्चिका कर्ण तंत्र सक्रिय")


    def पथ(self, नाम):

        return os.path.join(self.मूलपथ, नाम)


    def लेखन(self, नाम, डेटा):

        पूर्णपथ = self.पथ(नाम)

        with open(पूर्णपथ, "w", encoding="utf-8") as f:

            f.write(डेटा)

        print("सञ्चिका लिखित:", नाम)


    def पठन(self, नाम):

        पूर्णपथ = self.पथ(नाम)

        if not os.path.exists(पूर्णपथ):

            print("त्रुटि: सञ्चिका नहीं मिली")

            return None


        with open(पूर्णपथ, "r", encoding="utf-8") as f:

            डेटा = f.read()

        print("सञ्चिका पढ़ी:", नाम)

        return डेटा


    def सूची(self):

        files = os.listdir(self.मूलपथ)

        print("सञ्चिका सूची:")

        for f in files:

            print("•", f)


    def विलोपन(self, नाम):

        पूर्णपथ = self.पथ(नाम)

        if os.path.exists(पूर्णपथ):

            os.remove(पूर्णपथ)

            print("सञ्चिका हटाई:", नाम)
