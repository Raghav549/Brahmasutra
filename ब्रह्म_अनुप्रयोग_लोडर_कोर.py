# 🕉️ ब्रह्म अनुप्रयोग लोडर कोर VERSION 22

import os

class ब्रह्मअनुप्रयोगलोडरकोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग लोडर कोर सक्रिय")

        self.मूल_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_अनुप्रयोग")

        self.अस्थायी_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_temp")

        if not os.path.exists(self.अस्थायी_पथ):

            os.makedirs(self.अस्थायी_पथ)

        try:

            from ब्रह्म_निष्पादक import ब्रह्मनिष्पादक

            self.निष्पादक = ब्रह्मनिष्पादक()

        except Exception as e:

            print("त्रुटि: निष्पादक लोड नहीं हुआ:", e)

            self.निष्पादक = None


    def अनुप्रयोग_पथ_प्राप्त(self, नाम):

        if नाम.endswith(".ब्रह्म"):

            पूर्ण = os.path.join(self.मूल_पथ, नाम)

        else:

            पूर्ण = os.path.join(self.मूल_पथ, नाम + ".ब्रह्म")

        return पूर्ण


    def लोड(self, नाम):

        पथ = self.अनुप्रयोग_पथ_प्राप्त(नाम)

        if not os.path.exists(पथ):

            print("त्रुटि: अनुप्रयोग नहीं मिला:", पथ)

            return None

        print("अनुप्रयोग लोड:", पथ)

        try:

            with open(पथ, "r", encoding="utf-8") as f:

                code = f.read()

            temp = os.path.join(self.अस्थायी_पथ, "temp.ब्रह्म")

            with open(temp, "w", encoding="utf-8") as t:

                t.write(code)

            return temp

        except Exception as e:

            print("लोड त्रुटि:", e)

            return None


    def निष्पादन(self, नाम):

        if self.निष्पादक is None:

            print("त्रुटि: निष्पादक उपलब्ध नहीं")

            return

        temp = self.लोड(नाम)

        if temp is None:

            return

        print("निष्पादन प्रारम्भ:", temp)

        try:

            self.निष्पादक.निष्पादन(temp)

        except Exception as e:

            print("निष्पादन त्रुटि:", e)
