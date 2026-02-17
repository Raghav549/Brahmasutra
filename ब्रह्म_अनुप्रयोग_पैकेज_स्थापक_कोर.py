# 🕉️ ब्रह्म अनुप्रयोग पैकेज स्थापित कोर VERSION 26

import os
import zipfile
import shutil


class ब्रह्मअनुप्रयोगपैकेजस्थापककोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग पैकेज स्थापक कोर सक्रिय")

        self.स्थापित_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_स्थापित")

        if not os.path.exists(self.स्थापित_पथ):

            os.makedirs(self.स्थापित_पथ)


    def स्थापना(self, पैकेज_पथ):

        if not os.path.exists(पैकेज_पथ):

            print("त्रुटि: पैकेज नहीं मिला")

            return None

        नाम = os.path.basename(पैकेज_पथ).replace(".ब्रह्मपैक","")

        लक्ष्य = os.path.join(self.स्थापित_पथ, नाम)

        try:

            if os.path.exists(लक्ष्य):

                shutil.rmtree(लक्ष्य)

            os.makedirs(लक्ष्य)

            with zipfile.ZipFile(पैकेज_पथ,'r') as zipf:

                zipf.extractall(लक्ष्य)

            print("स्थापना सफल:", नाम)

            return लक्ष्य

        except Exception as e:

            print("स्थापना त्रुटि:", e)

            return None


    def सूची(self):

        print("स्थापित अनुप्रयोग:")

        files = os.listdir(self.स्थापित_पथ)

        if not files:

            print("कोई स्थापित अनुप्रयोग नहीं")

            return

        for f in files:

            print("•", f)
