import os

class ब्रह्मद्विआधारीनिर्माता:

    def __init__(self):

        self.output_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_द्विआधारी"
        )

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        print("🕉️ ब्रह्म द्विआधारी निर्माता सक्रिय")


    def निर्मित(self, कार्यक्रम_पथ):

        if not os.path.exists(कार्यक्रम_पथ):
            print("त्रुटि: कार्यक्रम नहीं मिला")
            return None

        नाम = os.path.basename(कार्यक्रम_पथ).replace(
            ".कार्यक्रम",".ब्रह्मबिन"
        )

        binary_path = os.path.join(
            self.output_dir,
            नाम
        )

        with open(कार्यक्रम_पथ,"r",encoding="utf-8") as f:
            code = f.read()

        binary_data = code.encode("utf-8")

        with open(binary_path,"wb") as f:
            f.write(binary_data)

        print("द्विआधारी निर्मित:", binary_path)

        return binary_path
