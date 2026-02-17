# 🕉️ BRAHMA AUTO APP CREATOR

import os

class ब्रह्मस्वतःनिर्माता:

    def __init__(self):
        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        if not os.path.exists(self.base):
            os.makedirs(self.base)

        print("🕉️ ब्रह्म स्वतः निर्माता सक्रिय")

    def निर्माण(self, नाम):

        app_path = os.path.join(self.base, नाम)

        if not os.path.exists(app_path):
            os.makedirs(app_path)

        main_file = os.path.join(app_path, "मुख्य.ब्रह्म")

        code = f'''
print("🕉️ {नाम} अनुप्रयोग प्रारंभ")

def मुख्य():
    print("🕉️ {नाम} सफलतापूर्वक चल रहा है")

मुख्य()
'''

        with open(main_file, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"🕉️ अनुप्रयोग निर्मित: {नाम}")

        return app_path
