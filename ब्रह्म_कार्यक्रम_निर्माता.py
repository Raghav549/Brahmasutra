# ब्रह्म कार्यक्रम निर्माता v15

import os

print("🕉️ ब्रह्म कार्यक्रम निर्माता सक्रिय")

class ब्रह्मकार्यक्रमनिर्माता:

    def __init__(self):

        self.output_dir = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_कार्यक्रम"

        os.makedirs(self.output_dir, exist_ok=True)

    def निर्माण(self, app_path, name):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return

        output_file = os.path.join(self.output_dir, name + ".कार्यक्रम")

        with open(output_file, "w", encoding="utf-8") as out:

            out.write("ब्रह्मकार्यक्रमV1\n")

            files = [
                "विन्यास.ब्रह्म",
                "पृष्ठभूमि.ब्रह्म",
                "अंतरफलक.ब्रह्म",
                "मुख्य.ब्रह्म"
            ]

            for file in files:

                full = os.path.join(app_path, file)

                if os.path.exists(full):

                    out.write("FILE_START\n")

                    with open(full, "r", encoding="utf-8") as f:

                        out.write(f.read())

                    out.write("\nFILE_END\n")

        print("कार्यक्रम निर्मित:", output_file)

        return output_file
