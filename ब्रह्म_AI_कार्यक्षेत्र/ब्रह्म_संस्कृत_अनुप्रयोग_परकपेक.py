# ब्रह्म संस्कृत अनुप्रयोग परकपेक
# VERSION 101 FIX

class ब्रह्मसंस्कृतअनुप्रयोगपरकपेक:

    def __init__(self):

        print("ब्रह्म अनुप्रयोग परकपेक सक्रिय")


    def परकपेकित(self, path):

        print(f"परकपेकण प्रारंभ: {path}")

        try:

            with open(path, "r", encoding="utf-8") as f:

                code = f.read()

            exec(code, globals())

            print("अनुप्रयोग सफलतापूर्वक निष्पादित")

            return True

        except Exception as e:

            print(f"त्रुटि: {e}")

            return False
