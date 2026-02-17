# 🕉️ ब्रह्म अनुप्रयोग स्थापक कोर VERSION 23

import os
import shutil

from ब्रह्म_अनुप्रयोग_लोडर_कोर import ब्रह्मअनुप्रयोगलोडरकोर


class ब्रह्मअनुप्रयोगस्थापककोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग स्थापक कोर सक्रिय")

        self.स्थापित_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_स्थापित")

        if not os.path.exists(self.स्थापित_पथ):

            os.makedirs(self.स्थापित_पथ)

        self.loader = ब्रह्मअनुप्रयोगलोडरकोर()


    def स्थापना(self, स्रोत_पथ):

        if not os.path.exists(स्रोत_पथ):

            print("त्रुटि: स्रोत अनुप्रयोग नहीं मिला")

            return

        नाम = os.path.basename(स्रोत_पथ)

        लक्ष्य = os.path.join(self.स्थापित_पथ, नाम)

        try:

            shutil.copy(स्रोत_पथ, लक्ष्य)

            print("स्थापित:", नाम)

        except Exception as e:

            print("स्थापना त्रुटि:", e)


    def सूची(self):

        print("स्थापित अनुप्रयोग:")

        files = os.listdir(self.स्थापित_पथ)

        if not files:

            print("कोई अनुप्रयोग नहीं")

            return

        for f in files:

            print("•", f)


    def निष्पादन(self, नाम):

        path = os.path.join(self.स्थापित_पथ, नाम)

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")

            return

        print("अनुप्रयोग निष्पादन:", नाम)

        self.loader.निष्पादन(path)
