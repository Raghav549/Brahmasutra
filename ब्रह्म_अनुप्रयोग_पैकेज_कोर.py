# 🕉️ ब्रह्म अनुप्रयोग पैकेज निर्माता कोर VERSION 25

import os
import zipfile


class ब्रह्मअनुप्रयोगपैकेजकोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग पैकेज कोर सक्रिय")

        self.पैकेज_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_पैकेज")

        if not os.path.exists(self.पैकेज_पथ):

            os.makedirs(self.पैकेज_पथ)


    def पैकेज_निर्माण(self, अनुप्रयोग_फोल्डर):

        if not os.path.exists(अनुप्रयोग_फोल्डर):

            print("त्रुटि: अनुप्रयोग फोल्डर नहीं मिला")

            return None

        नाम = os.path.basename(अनुप्रयोग_फोल्डर)

        पैकेज_नाम = नाम + ".ब्रह्मपैक"

        पैकेज_पूर्णपथ = os.path.join(self.पैकेज_पथ, पैकेज_नाम)

        try:

            with zipfile.ZipFile(पैकेज_पूर्णपथ, 'w') as zipf:

                for root, dirs, files in os.walk(अनुप्रयोग_फोल्डर):

                    for file in files:

                        पूर्णपथ = os.path.join(root, file)

                        सापेक्ष = os.path.relpath(पूर्णपथ, अनुप्रयोग_फोल्डर)

                        zipf.write(पूर्णपथ, सापेक्ष)

            print("पैकेज निर्मित:", पैकेज_पूर्णपथ)

            return पैकेज_पूर्णपथ

        except Exception as e:

            print("पैकेज त्रुटि:", e)

            return None


    def सूची(self):

        print("उपलब्ध पैकेज:")

        files = os.listdir(self.पैकेज_पथ)

        if not files:

            print("कोई पैकेज नहीं")

            return

        for f in files:

            print("•", f)
