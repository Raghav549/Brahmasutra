import os


class ब्रह्मअनुप्रयोगप्रक्षेपक:


    def __init__(self):

        self.install_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/स्थापित_अनुप्रयोग"
        )

        print("ब्रह्म अनुप्रयोग प्रक्षेपक सक्रिय")



    def प्रक्षेपित(self, app_name):

        app_path = os.path.join(self.install_dir, app_name)


        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")

            return False


        try:

            with open(app_path, "r", encoding="utf-8") as f:

                code = f.read()


            print("प्रक्षेपण:", app_name)


            exec(code, {})

            return True


        except Exception as e:

            print("प्रक्षेपण त्रुटि:", e)

            return False



    def सूची(self):

        return os.listdir(self.install_dir)
