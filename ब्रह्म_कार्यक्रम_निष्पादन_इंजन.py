# 🕉️ BRAHMA PROGRAM EXECUTION ENGINE VERSION 72

import os

class ब्रह्मकार्यक्रमनिष्पादनइंजन:

    def __init__(self):

        print("🕉️ ब्रह्म कार्यक्रम निष्पादन इंजन सक्रिय")

        self.base_path = os.path.expanduser("~/सूत्र-तंत्र")

        self.allowed_extensions = [

            ".ब्रह्म",
            ".कार्यक्रम",
            ".अनुप्रयोग"

        ]


    def सत्यापन(self, path):

        if not os.path.exists(path):

            print("त्रुटि: कार्यक्रम नहीं मिला")
            return False

        ext = os.path.splitext(path)[1]

        if ext not in self.allowed_extensions:

            print("त्रुटि: अमान्य कार्यक्रम प्रकार")
            return False

        return True


    def लोड(self, path):

        print("लोड हो रहा है:", path)

        with open(path, "r", encoding="utf-8") as f:

            return f.readlines()


    def निष्पादन(self, path):

        full_path = path

        if not os.path.isabs(path):

            full_path = os.path.join(self.base_path, path)

        if not self.सत्यापन(full_path):

            return

        code = self.लोड(full_path)

        print("निष्पादन प्रारम्भ")

        for line in code:

            line = line.strip()

            if line == "":
                continue

            print(">>", line)

        print("निष्पादन पूर्ण")
