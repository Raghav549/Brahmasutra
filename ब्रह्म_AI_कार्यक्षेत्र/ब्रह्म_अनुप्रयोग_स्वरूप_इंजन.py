import os


class ब्रह्मअनुप्रयोगस्वरूपइंजन:


    def __init__(self):

        self.समर्थित_स्वरूप = ".ब्रह्म"

        print("ब्रह्म अनुप्रयोग स्वरूप इंजन सक्रिय")


    def सत्यापित(self, path):

        if not path.endswith(self.समर्थित_स्वरूप):

            print("त्रुटि: असमर्थित स्वरूप")

            return False


        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return False


        return True


    def लोड(self, path):

        if not self.सत्यापित(path):

            return None


        try:

            with open(path, "r", encoding="utf-8") as file:

                data = file.read()


            print("अनुप्रयोग लोड सफल")

            return data


        except Exception as e:

            print("लोड त्रुटि:", e)

            return None


    def जानकारी(self, path):

        if not self.सत्यापित(path):

            return None


        size = os.path.getsize(path)

        return {

            "पथ": path,

            "आकार": size,

            "स्वरूप": self.समर्थित_स्वरूप

        }
