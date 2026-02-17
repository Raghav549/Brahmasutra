import os


class ब्रह्मसंस्कृतसञ्चिकातंत्र:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत सञ्चिका तंत्र सक्रिय")

        self.root = os.getcwd()


    def निर्माण(self, नाम):

        path = os.path.join(self.root, नाम)

        open(path, "w", encoding="utf-8").close()

        return f"सञ्चिका निर्मित: {नाम}"


    def लेखन(self, नाम, सामग्री):

        path = os.path.join(self.root, नाम)

        with open(path, "w", encoding="utf-8") as f:

            f.write(सामग्री)

        return f"लेखन पूर्ण: {नाम}"


    def पठन(self, नाम):

        path = os.path.join(self.root, नाम)

        with open(path, "r", encoding="utf-8") as f:

            data = f.read()

        return data


    def सूची(self):

        files = os.listdir(self.root)

        return files
