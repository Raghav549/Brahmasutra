# ब्रह्म फाइल प्रणाली

import os


class ब्रह्मफाइलप्रणाली:

    def __init__(self):

        self.मूल_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_FS")

        if not os.path.exists(self.मूल_पथ):
            os.makedirs(self.मूल_पथ)

        print("📁 ब्रह्म फाइल प्रणाली सक्रिय")


    def पूर्ण_पथ(self, नाम):

        return os.path.join(self.मूल_पथ, नाम)


    def लिखो(self, नाम, सामग्री):

        path = self.पूर्ण_पथ(नाम)

        with open(path, "w", encoding="utf-8") as f:
            f.write(सामग्री)

        return {
            "status": "success",
            "file": नाम
        }


    def पढ़ो(self, नाम):

        path = self.पूर्ण_पथ(नाम)

        if not os.path.exists(path):

            return {
                "status": "error",
                "message": "file not found"
            }

        with open(path, "r", encoding="utf-8") as f:

            data = f.read()

        return {
            "status": "success",
            "data": data
        }


    def हटाओ(self, नाम):

        path = self.पूर्ण_पथ(नाम)

        if os.path.exists(path):

            os.remove(path)

            return {
                "status": "success"
            }

        return {
            "status": "error"
        }


    def सूची(self):

        return os.listdir(self.मूल_पथ)
