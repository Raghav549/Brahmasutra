# 🕉️ ब्रह्म Prompt अनुप्रयोग निर्माता

from ब्रह्म_अनुप्रयोग_निर्माण_कोर import ब्रह्मअनुप्रयोगनिर्माणकोर


class ब्रह्मप्रॉम्प्टअनुप्रयोगनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म Prompt अनुप्रयोग निर्माता सक्रिय")

        self.builder = ब्रह्मअनुप्रयोगनिर्माणकोर()


    def विश्लेषण(self, prompt):

        print("Prompt विश्लेषण:", prompt)

        code = ""

        if "login" in prompt or "लॉगिन" in prompt:

            code += """
स्थापित लॉगिन 1
दर्शय लॉगिन
"""


        if "database" in prompt or "डेटाबेस" in prompt:

            code += """
स्थापित डेटाबेस 1
दर्शय डेटाबेस
"""


        if "api" in prompt or "API" in prompt:

            code += """
स्थापित API 1
दर्शय API
"""


        if "dashboard" in prompt or "डैशबोर्ड" in prompt:

            code += """
स्थापित डैशबोर्ड 1
दर्शय डैशबोर्ड
"""


        if code == "":
            code = """
स्थापित अ 999
दर्शय अ
"""

        return code


    def निर्माण(self, prompt):

        app_name = prompt.replace(" ", "_")

        code = self.विश्लेषण(prompt)

        path = self.builder.निर्माण(app_name, code)

        print("Prompt से अनुप्रयोग निर्मित:", path)

        return path


# test
if __name__ == "__main__":

    creator = ब्रह्मप्रॉम्प्टअनुप्रयोगनिर्माता()

    prompt = input("Prompt लिखें: ")

    creator.निर्माण(prompt)
