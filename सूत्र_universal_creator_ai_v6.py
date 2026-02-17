import os
import random
import datetime

class सूत्रUniversalCreatorAIv6:

    def __init__(self):

        print("🕉️ सूत्र Universal Creator AI v6 सक्रिय")
        print("पूर्ण अनुप्रयोग निर्माण तंत्र तैयार")


    def प्रारम्भ(self):

        while True:

            prompt = input("CreatorAIv6 >>> ")

            if prompt.strip() == "निर्गम":

                print("CreatorAI बन्द")
                break

            self.निर्माण(prompt)


    def नाम_प्राप्त(self,prompt):

        words = prompt.split()

        ignore = ["बनाओ","create","make","website","app","ai","software"]

        for w in words[::-1]:

            if w.lower() not in ignore:

                return w

        return "प्रणाली"+str(random.randint(1000,9999))


    def निर्माण(self,prompt):

        name = self.नाम_प्राप्त(prompt)

        print("निर्माण प्रारम्भ:",name)

        if "website" in prompt.lower():

            self.website(name)

        elif "app" in prompt.lower():

            self.app(name)

        elif "ai" in prompt.lower():

            self.ai(name)

        elif "software" in prompt.lower():

            self.software(name)

        else:

            self.software(name)


    def website(self,name):

        folder = name+"_website"

        os.makedirs(folder+"/assets",exist_ok=True)

        os.makedirs(folder+"/backend",exist_ok=True)

        html = f"""
<html>
<head>
<title>{name}</title>
</head>
<body>
<h1>{name} Website</h1>
<p>सूत्र Universal Creator AI द्वारा निर्मित</p>
</body>
</html>
"""

        with open(folder+"/index.html","w",encoding="utf-8") as f:
            f.write(html)

        with open(folder+"/backend/server.py","w",encoding="utf-8") as f:
            f.write("print('सूत्र Backend सक्रिय')")

        print("Website निर्माण पूर्ण:",folder)


    def app(self,name):

        folder = name+"_app"

        os.makedirs(folder+"/core",exist_ok=True)
        os.makedirs(folder+"/ui",exist_ok=True)

        with open(folder+"/core/main.सूत्र","w",encoding="utf-8") as f:
            f.write("दर्शय 'सूत्र App सक्रिय'")

        with open(folder+"/ui/layout.txt","w",encoding="utf-8") as f:
            f.write("UI संरचना")

        print("App निर्माण पूर्ण:",folder)


    def ai(self,name):

        folder = name+"_ai"

        os.makedirs(folder+"/model",exist_ok=True)
        os.makedirs(folder+"/brain",exist_ok=True)

        with open(folder+"/brain/core.py","w",encoding="utf-8") as f:
            f.write("print('सूत्र AI मस्तिष्क सक्रिय')")

        print("AI निर्माण पूर्ण:",folder)


    def software(self,name):

        folder = name+"_software"

        os.makedirs(folder+"/system",exist_ok=True)

        with open(folder+"/system/main.सूत्र","w",encoding="utf-8") as f:
            f.write("दर्शय 'सूत्र Software सक्रिय'")

        print("Software निर्माण पूर्ण:",folder)


creator = सूत्रUniversalCreatorAIv6()

creator.प्रारम्भ()
