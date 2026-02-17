# 🕉️ ब्रह्म सञ्चिका निष्पादन कोर VERSION 1

print("🕉️ ब्रह्म सञ्चिका निष्पादन कोर सक्रिय")

import os

from ब्रह्म_निष्पादन_कोर import ब्रह्मनिष्पादनकोर


class ब्रह्मसञ्चिकानिष्पादनकोर:

    def __init__(self):

        print("🕉️ ब्रह्म सञ्चिका निष्पादन प्रणाली तैयार")

        self.executor = ब्रह्मनिष्पादनकोर()


    def निष्पादन(self, path):

        if not os.path.exists(path):

            print("त्रुटि: सञ्चिका नहीं मिली")
            return

        print("सञ्चिका लोड:", path)

        with open(path, "r", encoding="utf-8") as f:

            lines = f.readlines()

        print("निष्पादन प्रारम्भ")

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            self.executor.आदेश_चलाओ(line)

        print("निष्पादन पूर्ण")


# test
if __name__ == "__main__":

    core = ब्रह्मसञ्चिकानिष्पादनकोर()

    core.निष्पादन("परीक्षण.ब्रह्म")
