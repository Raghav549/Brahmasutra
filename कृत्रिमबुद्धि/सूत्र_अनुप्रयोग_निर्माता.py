import os
import random


class सूत्रअनुप्रयोगनिर्माता:


    def __init__(self):

        print("🕉️ सूत्र अनुप्रयोग निर्माता कृत्रिमबुद्धि सक्रिय")

        self.अनुप्रयोग_पथ = "निर्मित_अनुप्रयोग"

        if not os.path.exists(self.अनुप्रयोग_पथ):

            os.mkdir(self.अनुप्रयोग_पथ)


    def नाम_निर्माण(self):

        return "अनुप्रयोग_" + str(random.randint(1000,9999))


    def सूत्र_अनुप्रयोग(self, नाम):

        पथ = self.अनुप्रयोग_पथ + "/" + नाम + ".सूत्र"

        with open(पथ,"w",encoding="utf-8") as f:

            f.write("संकल्प अ 10\n")

            f.write("संकल्प ब 20\n")

            f.write("योग अ ब\n")

            f.write("दर्शय अ\n")

            f.write("निर्गम\n")


        print("सूत्र अनुप्रयोग निर्मित:", पथ)


    def वेबसाइट(self, नाम):

        पथ = self.अनुप्रयोग_पथ + "/" + नाम + ".html"

        html = f"""
<html>
<head>
<title>{नाम}</title>
</head>
<body>
<h1>🕉️ सूत्र निर्मित वेबसाइट</h1>
<p>अनुप्रयोग नाम: {नाम}</p>
</body>
</html>
"""

        with open(पथ,"w",encoding="utf-8") as f:

            f.write(html)


        print("वेबसाइट निर्मित:", पथ)


    def स्वचालन(self, नाम):

        पथ = self.अनुप्रयोग_पथ + "/" + नाम + ".py"

        code = f"""
print("🕉️ स्वचालन प्रारम्भ")
print("अनुप्रयोग: {नाम}")
"""

        with open(पथ,"w",encoding="utf-8") as f:

            f.write(code)


        print("स्वचालन निर्मित:", पथ)


    def निर्माण(self, प्रकार):

        नाम = self.नाम_निर्माण()

        if प्रकार == "सूत्र":

            self.सूत्र_अनुप्रयोग(नाम)

        elif प्रकार == "वेबसाइट":

            self.वेबसाइट(नाम)

        elif प्रकार == "स्वचालन":

            self.स्वचालन(नाम)

        else:

            print("अज्ञात प्रकार")
