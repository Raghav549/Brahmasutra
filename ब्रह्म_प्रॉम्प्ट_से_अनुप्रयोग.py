# 🕉️ BRAHMA PROMPT TO APP GENERATOR

import os

class ब्रह्मप्रॉम्प्टअनुप्रयोग:

    def __init__(self):
        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        if not os.path.exists(self.base):
            os.makedirs(self.base)

        print("🕉️ ब्रह्म प्रॉम्प्ट अनुप्रयोग जनरेटर सक्रिय")

    def निर्माण(self, प्रॉम्प्ट):

        नाम = प्रॉम्प्ट.replace(" ", "_")

        path = os.path.join(self.base, नाम)

        if not os.path.exists(path):
            os.makedirs(path)

        file = os.path.join(path, "मुख्य.ब्रह्म")

        code = f'''
print("🕉️ अनुप्रयोग प्रारंभ: {प्रॉम्प्ट}")

def मुख्य():
    print("🕉️ प्रॉम्प्ट आधारित अनुप्रयोग चल रहा है")
    print("🕉️ विवरण:", "{प्रॉम्प्ट}")

मुख्य()
'''

        with open(file, "w", encoding="utf-8") as f:
            f.write(code)

        print("🕉️ प्रॉम्प्ट से अनुप्रयोग निर्मित:", नाम)

        return नाम
