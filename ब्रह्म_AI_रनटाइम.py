# 🕉️ BRAHMA AI VERSION 10
# Full Runtime Execution Engine

import os

class ब्रह्मAIRuntime:

    def __init__(self):

        print("🕉️ ब्रह्म AI रनटाइम VERSION 10 सक्रिय")

        self.root = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")


    def चलाओ(self, app_name):

        main_file = os.path.join(self.root, app_name, "मुख्य.ब्रह्म")

        if not os.path.exists(main_file):

            print("त्रुटि: मुख्य अनुप्रयोग नहीं मिला")
            return


        print("अनुप्रयोग प्रारम्भ:", app_name)


        with open(main_file, "r", encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            line = line.strip()

            if line.startswith("दर्शय"):

                text = line.replace("दर्शय", "").strip()

                print("मॉड्यूल:", text)


        print("अनुप्रयोग निष्पादन पूर्ण")


if __name__ == "__main__":

    runtime = ब्रह्मAIRuntime()

    name = input("अनुप्रयोग नाम: ")

    runtime.चलाओ(name)
