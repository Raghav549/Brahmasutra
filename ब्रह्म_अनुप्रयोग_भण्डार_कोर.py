# 🕉️ ब्रह्म अनुप्रयोग भण्डार कोर VERSION 24

import os
import shutil


class ब्रह्मअनुप्रयोगभण्डारकोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग भण्डार कोर सक्रिय")

        self.भण्डार_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_भण्डार")

        if not os.path.exists(self.भण्डार_पथ):

            os.makedirs(self.भण्डार_पथ)


    def जोड़ें(self, अनुप्रयोग_पथ):

        if not os.path.exists(अनुप्रयोग_पथ):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return

        नाम = os.path.basename(अनुप्रयोग_पथ)

        लक्ष्य = os.path.join(self.भण्डार_पथ, नाम)

        try:

            shutil.copy(अनुप्रयोग_पथ, लक्ष्य)

            print("भण्डार में जोड़ा:", नाम)

        except Exception as e:

            print("भण्डार त्रुटि:", e)


    def सूची(self):

        print("भण्डार अनुप्रयोग:")

        files = os.listdir(self.भण्डार_पथ)

        if not files:

            print("भण्डार खाली है")

            return

        for f in files:

            print("•", f)


    def प्राप्त(self, नाम, लक्ष्य_पथ):

        स्रोत = os.path.join(self.भण्डार_पथ, नाम)

        if not os.path.exists(स्रोत):

            print("त्रुटि: अनुप्रयोग भण्डार में नहीं मिला")

            return

        लक्ष्य = os.path.join(लक्ष्य_पथ, नाम)

        try:

            shutil.copy(स्रोत, लक्ष्य)

            print("प्राप्त:", नाम)

        except Exception as e:

            print("प्राप्त त्रुटि:", e)
