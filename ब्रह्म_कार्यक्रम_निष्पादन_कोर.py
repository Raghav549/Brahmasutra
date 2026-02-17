# 🕉️ ब्रह्म कार्यक्रम निष्पादन कोर
# VERSION 15

print("🕉️ ब्रह्म कार्यक्रम निष्पादन कोर सक्रिय")

import os

from ब्रह्म_आदेश_निष्पादन_कोर import ब्रह्मआदेशनिष्पादनकोर


class ब्रह्मकार्यक्रमनिष्पादनकोर:

    def __init__(self):

        self.executor = ब्रह्मआदेशनिष्पादनकोर()

        print("कार्यक्रम निष्पादन प्रणाली तैयार")


    def कार्यक्रम_चलाओ(self, संचिका):

        print("कार्यक्रम लोड:", संचिका)

        if not os.path.exists(संचिका):

            print("त्रुटि: कार्यक्रम नहीं मिला")

            return


        print("कार्यक्रम निष्पादन प्रारम्भ")


        with open(संचिका, "r", encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            line = line.strip()

            if line == "":
                continue

            if line.startswith("#"):
                continue

            self.executor.आदेश_चलाओ(line)


        print("कार्यक्रम निष्पादन पूर्ण")


# TEST
if __name__ == "__main__":

    core = ब्रह्मकार्यक्रमनिष्पादनकोर()

    test_file = "परीक्षण.ब्रह्म"

    with open(test_file, "w", encoding="utf-8") as f:

        f.write("""
# BRAHMA PROGRAM TEST

स्थापित अ 50
स्थापित ब 25
योग अ ब
दर्शय अ

गुणा अ ब
दर्शय अ
""")

    core.कार्यक्रम_चलाओ(test_file)
