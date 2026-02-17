import subprocess
import os


class ब्रह्मअनुप्रयोगप्रक्षेपक:

    def __init__(self):

        print("ब्रह्म अनुप्रयोग प्रक्षेपक सक्रिय")


    def प्रक्षेपित(self, path):

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला:", path)

            return False


        print("अनुप्रयोग प्रक्षेपित:", path)


        try:

            subprocess.run(["python", path])

            print("अनुप्रयोग सफलतापूर्वक प्रारंभ")

            return True


        except Exception as e:

            print("प्रक्षेपण त्रुटि:", e)

            return False
