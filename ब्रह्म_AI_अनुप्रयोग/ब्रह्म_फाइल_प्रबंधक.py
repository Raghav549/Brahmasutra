# ब्रह्म फाइल प्रबंधक
# VERSION 54

import os


class ब्रह्मफाइलप्रबंधक:

    def __init__(self):

        self.root = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_storage")

        os.makedirs(self.root, exist_ok=True)

        print("🕉️ ब्रह्म फाइल प्रबंधक सक्रिय")


    def बनाएं(self, नाम, डेटा):

        path = os.path.join(self.root, नाम)

        with open(path, "w", encoding="utf-8") as f:
            f.write(डेटा)

        return {
            "status": "success",
            "file": नाम
        }


    def पढ़ें(self, नाम):

        path = os.path.join(self.root, नाम)

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


    def हटाएं(self, नाम):

        path = os.path.join(self.root, नाम)

        if os.path.exists(path):

            os.remove(path)

            return {
                "status": "success"
            }

        return {
            "status": "error",
            "message": "file not found"
        }


    def सूची(self):

        return os.listdir(self.root)
