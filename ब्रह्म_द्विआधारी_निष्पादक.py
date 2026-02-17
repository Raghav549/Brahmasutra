import os
from ब्रह्म_निष्पादक import ब्रह्मनिष्पादक

class ब्रह्मद्विआधारीनिष्पादक:

    def __init__(self):

        print("🕉️ ब्रह्म द्विआधारी निष्पादक सक्रिय")

        self.executor = ब्रह्मनिष्पादक()


    def निष्पादन(self, binary_path):

        if not os.path.exists(binary_path):

            print("त्रुटि: द्विआधारी नहीं मिला")

            return


        with open(binary_path,"rb") as f:

            code = f.read().decode("utf-8")


        temp_path = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_temp_binary.ब्रह्म"
        )


        with open(temp_path,"w",encoding="utf-8") as f:

            f.write(code)


        print("द्विआधारी लोड सफल")

        print("ब्रह्म निष्पादन प्रारम्भ")


        self.executor.निष्पादन(temp_path)


        print("द्विआधारी निष्पादन पूर्ण")
