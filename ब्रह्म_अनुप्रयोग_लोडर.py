# 🕉️ ब्रह्म अनुप्रयोग लोडर

import os

from ब्रह्म_कार्यक्रम_लोडर import ब्रह्मकार्यक्रमलोडर


class ब्रह्मअनुप्रयोगलोडर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग लोडर सक्रिय")

        self.program_loader = ब्रह्मकार्यक्रमलोडर()


    def निष्पादन(self, path):

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return


        print("अनुप्रयोग लोड हो रहा है:", path)

        self.program_loader.निष्पादन(path)
