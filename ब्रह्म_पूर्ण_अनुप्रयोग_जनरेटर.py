# 🕉️ BRAHMA FULL APP GENERATOR

import os

class ब्रह्मपूर्णअनुप्रयोगजनरेटर:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        if not os.path.exists(self.base):
            os.makedirs(self.base)

        print("🕉️ ब्रह्म पूर्ण अनुप्रयोग जनरेटर सक्रिय")

    def निर्माण(self, नाम):

        app_path = os.path.join(self.base, नाम)

        folders = [
            "backend",
            "frontend",
            "database",
            "api"
        ]

        os.makedirs(app_path, exist_ok=True)

        for folder in folders:
            os.makedirs(os.path.join(app_path, folder), exist_ok=True)

        main_file = os.path.join(app_path, "मुख्य.ब्रह्म")

        code = f'''
print("🕉️ पूर्ण अनुप्रयोग प्रारंभ")

def प्रारंभ():
    print("backend सक्रिय")
    print("frontend सक्रिय")
    print("database सक्रिय")
    print("api सक्रिय")

प्रारंभ()
'''

        with open(main_file, "w", encoding="utf-8") as f:
            f.write(code)

        print("🕉️ पूर्ण अनुप्रयोग निर्मित:", नाम)

        return नाम
