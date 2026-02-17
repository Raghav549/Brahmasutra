import os


class ब्रह्मसंस्कृतअनुप्रयोगप्रक्षेपक:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत अनुप्रयोग प्रक्षेपक सक्रिय")

        self.root = os.getcwd()

        self.install_dir = os.path.join(self.root, "स्थापित")


    def सूची(self):

        if not os.path.exists(self.install_dir):

            print("कोई अनुप्रयोग स्थापित नहीं")

            return


        apps = os.listdir(self.install_dir)

        print("स्थापित अनुप्रयोग:")

        for app in apps:

            print("•", app)


    def संस्कृत_कोड_परिवर्तन(self, code):

        lines = code.split("\n")

        converted = []


        for line in lines:

            line = line.strip()


            if line.startswith("दर्शय"):

                text = line.replace("दर्शय", "", 1).strip()

                converted.append(f'print("{text}")')


            elif line == "":

                converted.append("")


            else:

                converted.append(line)


        return "\n".join(converted)


    def प्रक्षेपण(self, app_name):

        app_path = os.path.join(self.install_dir, app_name)


        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return


        main_file = None


        for file in os.listdir(app_path):

            if file.endswith(".ब्रह्म"):

                main_file = os.path.join(app_path, file)

                break


        if not main_file:

            print("त्रुटि: मुख्य file नहीं मिली")

            return


        print("प्रक्षेपण:", main_file)


        with open(main_file, encoding="utf-8") as f:

            code = f.read()


        safe_code = self.संस्कृत_कोड_परिवर्तन(code)


        exec(safe_code)
