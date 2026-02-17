# 🕉️ ब्रह्म अनुप्रयोग भण्डार प्रणाली

import os
import shutil

print("🕉️ ब्रह्म अनुप्रयोग भण्डार सक्रिय")


class ब्रह्मभण्डार:

    def __init__(self):

        self.भण्डार_पथ = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_भण्डार"
        )

        self.स्थापित_पथ = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_स्थापित"
        )

        os.makedirs(self.भण्डार_पथ, exist_ok=True)
        os.makedirs(self.स्थापित_पथ, exist_ok=True)


    def सूची(self):

        apps = os.listdir(self.भण्डार_पथ)

        print("📦 उपलब्ध अनुप्रयोग:")

        if not apps:
            print("कोई अनुप्रयोग नहीं")

        for app in apps:
            print("•", app)


    def स्थापना(self, नाम):

        स्रोत = os.path.join(self.भण्डार_पथ, नाम)

        if not os.path.exists(स्रोत):
            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return

        लक्ष्य = os.path.join(self.स्थापित_पथ, नाम)

        shutil.copy(स्रोत, लक्ष्य)

        print("स्थापित:", नाम)


    def हटाओ(self, नाम):

        लक्ष्य = os.path.join(self.स्थापित_पथ, नाम)

        if os.path.exists(लक्ष्य):

            os.remove(लक्ष्य)

            print("हटाया:", नाम)

        else:

            print("त्रुटि: अनुप्रयोग स्थापित नहीं है")


    def स्थापित_सूची(self):

        apps = os.listdir(self.स्थापित_पथ)

        print("💿 स्थापित अनुप्रयोग:")

        if not apps:
            print("कोई स्थापित अनुप्रयोग नहीं")

        for app in apps:
            print("•", app)
