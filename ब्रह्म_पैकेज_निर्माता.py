import os
import zipfile

class ब्रह्मपैकेजनिर्माता:

    def __init__(self):
        self.output_dir = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_पैकेज")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        print("🕉️ ब्रह्म पैकेज निर्माता सक्रिय")


    def निर्मित(self, कार्यक्रम_पथ):

        if not os.path.exists(कार्यक्रम_पथ):
            print("त्रुटि: कार्यक्रम नहीं मिला")
            return None

        नाम = os.path.basename(कार्यक्रम_पथ).replace(".कार्यक्रम","")

        पैकेज_पथ = os.path.join(
            self.output_dir,
            नाम + ".ब्रह्मपैक"
        )

        with zipfile.ZipFile(पैकेज_पथ,"w") as z:
            z.write(कार्यक्रम_पथ, "मुख्य.कार्यक्रम")

        print("पैकेज निर्मित:", पैकेज_पथ)

        return पैकेज_पथ
