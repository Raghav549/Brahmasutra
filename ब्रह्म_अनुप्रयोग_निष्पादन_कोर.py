import os

from brahma_paths import data_root
class ब्रह्मअनुप्रयोगनिष्पादनकोर:

    def __init__(self):

        self.स्थापित_पथ = data_root("ब्रह्म_स्थापित")

        print("🕉️ ब्रह्म अनुप्रयोग निष्पादन कोर सक्रिय")


    def निष्पादन(self, नाम):

        अनुप्रयोग_पथ = os.path.join(self.स्थापित_पथ, नाम)

        if not os.path.exists(अनुप्रयोग_पथ):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return


        print("अनुप्रयोग लोड:", नाम)


        files = os.listdir(अनुप्रयोग_पथ)


        मुख्य_फाइल = None


        # detect correct main file
        for file in files:

            if file == "मुख्य.ब्रह्म":

                मुख्य_फाइल = file

                break


        if मुख्य_फाइल is None:

            print("त्रुटि: मुख्य फ़ाइल नहीं मिली")

            return


        print("मुख्य फ़ाइल मिली:", मुख्य_फाइल)


        full_path = os.path.join(अनुप्रयोग_पथ, मुख्य_फाइल)


        with open(full_path, "r", encoding="utf-8") as f:

            lines = f.readlines()


        print("निष्पादन प्रारम्भ")


        for line in lines:

            line = line.strip()

            if line:

                print(">>", line)


        print("निष्पादन पूर्ण")
