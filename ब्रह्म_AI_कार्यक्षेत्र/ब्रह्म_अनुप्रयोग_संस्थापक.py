import os
import shutil


class ब्रह्मअनुप्रयोगसंस्थापक:


    def __init__(self):

        self.install_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/स्थापित_अनुप्रयोग"
        )

        if not os.path.exists(self.install_dir):

            os.makedirs(self.install_dir)


        print("ब्रह्म अनुप्रयोग संस्थापक सक्रिय")



    def स्थापित(self, source_path):

        if not os.path.exists(source_path):

            print("त्रुटि: स्रोत अनुप्रयोग नहीं मिला")

            return False


        if not source_path.endswith(".ब्रह्म"):

            print("त्रुटि: असमर्थित अनुप्रयोग स्वरूप")

            return False


        app_name = os.path.basename(source_path)

        destination = os.path.join(self.install_dir, app_name)


        try:

            shutil.copy(source_path, destination)

            print("अनुप्रयोग स्थापित:", app_name)

            return True


        except Exception as e:

            print("स्थापना त्रुटि:", e)

            return False



    def सूची(self):

        apps = os.listdir(self.install_dir)

        return apps



    def पथ(self, app_name):

        return os.path.join(self.install_dir, app_name)
