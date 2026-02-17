import os


class ब्रह्मसंस्कृतकार्यक्रमलोडर:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत कार्यक्रम लोडर सक्रिय")

        self.root = os.getcwd()


    def लोड(self, नाम):

        path = os.path.join(self.root, नाम)

        if not os.path.exists(path):

            return "त्रुटि: कार्यक्रम नहीं मिला"


        with open(path, "r", encoding="utf-8") as f:

            code = f.read()


        return code


    def निष्पादन(self, नाम):

        path = os.path.join(self.root, नाम)

        if not os.path.exists(path):

            return "त्रुटि: कार्यक्रम नहीं मिला"


        print(f"कार्यक्रम लोड: {नाम}")


        with open(path, "r", encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            line = line.strip()

            if line.startswith("दर्शय"):

                text = line.replace("दर्शय", "").strip()

                print(text)


        print("कार्यक्रम समाप्त")
