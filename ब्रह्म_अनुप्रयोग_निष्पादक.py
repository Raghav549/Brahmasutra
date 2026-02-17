# ब्रह्म अनुप्रयोग निष्पादक v14

import os

from ब्रह्म_निष्पादक import ब्रह्मनिष्पादक

print("🕉️ ब्रह्म अनुप्रयोग निष्पादक सक्रिय")

class ब्रह्मअनुप्रयोगनिष्पादक:

    def __init__(self):

        self.executor = ब्रह्मनिष्पादक()

    def निष्पादन(self, app_path):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return

        print("अनुप्रयोग प्रारम्भ:", app_path)

        files = [
            "विन्यास.ब्रह्म",
            "पृष्ठभूमि.ब्रह्म",
            "अंतरफलक.ब्रह्म",
            "मुख्य.ब्रह्म"
        ]

        for file in files:

            full = os.path.join(app_path, file)

            if os.path.exists(full):

                print("निष्पादन:", file)

                self.executor.निष्पादन(full)

        print("अनुप्रयोग समाप्त")
