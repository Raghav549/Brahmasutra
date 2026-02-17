import os

class सूत्रAppBuilderAIv4:

    def __init__(self):

        print("🕉️ सूत्र App Builder AI v4 सक्रिय")


    def प्रारम्भ(self):

        while True:

            prompt = input("AIv4 >>> ")

            if prompt.strip() == "निर्गम":

                break

            self.build(prompt)


    def get_name(self,prompt):

        words = prompt.split()

        ignore = ["बनाओ","create","make"]

        for w in words[::-1]:

            if w not in ignore and w!="website" and w!="app":

                return w

        return "अनुप्रयोग"


    def build(self,prompt):

        name = self.get_name(prompt)

        print("निर्माण:",name)

        if "website" in prompt:

            self.build_website(name)

        elif "app" in prompt:

            self.build_app(name)

        else:

            print("प्रकार अज्ञात")


    def build_website(self,name):

        folder = name+"_system"

        os.makedirs(folder,exist_ok=True)

        file = folder+"/index.html"

        with open(file,"w",encoding="utf-8") as f:

            f.write(f"<html><body><h1>{name} website ready</h1></body></html>")

        print("Website ready")

        print("पूर्ण निर्माण:",name)


    def build_app(self,name):

        folder = name+"_app"

        os.makedirs(folder,exist_ok=True)

        print("App ready")

        print("पूर्ण निर्माण:",name)



ai = सूत्रAppBuilderAIv4()

ai.प्रारम्भ()
