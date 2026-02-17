# 🕉️ BRAHMA AI VERSION 13
# Intelligent Logic Generator

import os

class ब्रह्मAITarkaNirmata:

    def __init__(self):

        print("🕉️ ब्रह्म AI तर्क निर्माता VERSION 13 सक्रिय")

        self.root = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        os.makedirs(self.root, exist_ok=True)


    def analyse_prompt(self, prompt):

        modules = []

        if "login" in prompt.lower():
            modules.append("लॉगिन")

        if "database" in prompt.lower():
            modules.append("डेटाबेस")

        if "api" in prompt.lower():
            modules.append("API")

        if "dashboard" in prompt.lower():
            modules.append("डैशबोर्ड")

        if "chat" in prompt.lower():
            modules.append("चैट")

        return modules


    def generate_logic(self, modules):

        logic = ""

        for module in modules:

            logic += f"दर्शय {module}_सक्रिय\n"

        return logic


    def write_file(self, path, content):

        with open(path, "w", encoding="utf-8") as f:

            f.write(content)


    def निर्मित(self, prompt):

        name = prompt.replace(" ", "_")

        app_path = os.path.join(self.root, name)

        os.makedirs(app_path, exist_ok=True)

        modules = self.analyse_prompt(prompt)

        logic = self.generate_logic(modules)

        main = "दर्शय अनुप्रयोग_प्रारम्भ\n" + logic

        self.write_file(app_path + "/मुख्य.ब्रह्म", main)

        print("तर्क आधारित अनुप्रयोग निर्मित:", app_path)

        return name


if __name__ == "__main__":

    ai = ब्रह्मAITarkaNirmata()

    prompt = input("Prompt लिखें: ")

    name = ai.निर्मित(prompt)

    print("सफल:", name)
