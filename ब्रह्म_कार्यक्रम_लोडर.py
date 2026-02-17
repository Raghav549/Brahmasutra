# ब्रह्म कार्यक्रम लोडर v16

import os

print("🕉️ ब्रह्म कार्यक्रम लोडर सक्रिय")

class ब्रह्मकार्यक्रमलोडर:

    def __init__(self):

        self.temp_dir = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_temp"

        os.makedirs(self.temp_dir, exist_ok=True)

    def निष्पादन(self, program_path):

        if not os.path.exists(program_path):

            print("त्रुटि: कार्यक्रम नहीं मिला")
            return

        print("कार्यक्रम लोड हो रहा है:", program_path)

        with open(program_path, "r", encoding="utf-8") as f:

            lines = f.readlines()

        current_file = None
        buffer = []

        files = []

        for line in lines:

            line = line.strip()

            if line == "FILE_START":

                buffer = []

            elif line == "FILE_END":

                files.append("\n".join(buffer))

            elif line != "ब्रह्मकार्यक्रमV1":

                buffer.append(line)

        # write temp main file

        main_path = os.path.join(self.temp_dir, "मुख्य.ब्रह्म")

        with open(main_path, "w", encoding="utf-8") as f:

            f.write("\n".join(files))

        print("कार्यक्रम निष्पादन प्रारम्भ")

        from ब्रह्म_निष्पादक import ब्रह्मनिष्पादक

        executor = ब्रह्मनिष्पादक()

        executor.निष्पादन(main_path)
