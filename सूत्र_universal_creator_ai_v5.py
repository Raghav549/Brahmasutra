import os
import random

class सूत्रUniversalCreatorAIv5:

    def __init__(self):

        print("🕉️ सूत्र Universal Creator AI v5 सक्रिय")


    def प्रारम्भ(self):

        while True:

            prompt = input("CreatorAIv5 >>> ")

            if prompt.strip() == "निर्गम":

                break

            self.निर्माण(prompt)


    def नाम_प्राप्त(self,prompt):

        words = prompt.split()

        ignore = ["बनाओ","create","make","software","website","app","ai"]

        for w in words[::-1]:

            if w not in ignore:

                return w

        return "प्रणाली"+str(random.randint(1000,9999))


    def निर्माण(self,prompt):

        name = self.नाम_प्राप्त(prompt)

        print("निर्माण प्रारम्भ:",name)

        if "website" in prompt:

            self.website(name)

        elif "app" in prompt:

            self.app(name)

        elif "ai" in prompt:

            self.ai(name)

        elif "software" in prompt:

            self.software(name)

        else:

            self.software(name)


    def website(self,name):

        folder = name+"_website"

        os.makedirs(folder,exist_ok=True)

        with open(folder+"/index.html","w",encoding="utf-8") as f:

            f.write(f"<html><body><h1>{name} website ready</h1></body></html>")

        print("Website निर्माण पूर्ण")


    def app(self,name):

        folder = name+"_app"

        os.makedirs(folder,exist_ok=True)

        with open(folder+"/app.सूत्र","w",encoding="utf-8") as f:

            f.write("दर्शय 'सूत्र App सक्रिय'")

        print("App निर्माण पूर्ण")


    def software(self,name):

        folder = name+"_software"

        os.makedirs(folder,exist_ok=True)

        with open(folder+"/main.सूत्र","w",encoding="utf-8") as f:

            f.write("दर्शय 'सूत्र Software सक्रिय'")

        print("Software निर्माण पूर्ण")


    def ai(self,name):

        folder = name+"_ai"

        os.makedirs(folder,exist_ok=True)

        with open(folder+"/brain.सूत्र","w",encoding="utf-8") as f:

            f.write("दर्शय 'सूत्र AI सक्रिय'")

        print("AI निर्माण पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global creator


    creator = सूत्रUniversalCreatorAIv5()

    creator.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
