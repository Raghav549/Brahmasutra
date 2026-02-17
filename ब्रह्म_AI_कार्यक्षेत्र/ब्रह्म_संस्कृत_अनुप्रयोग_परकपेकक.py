class ब्रह्मसंस्कृतअनुप्रयोगपरकपेकक:

    def __init__(self):

        print("ब्रह्म संस्कृत अनुप्रयोग परकपेकक सक्रिय")


    def परकपेकित(self, path):

        print("अनुप्रयोग परकपेकित:", path)

        try:

            with open(path, "r", encoding="utf-8") as f:

                code = f.read()

            exec(code, {})

            print("अनुप्रयोग सफलतापूर्वक प्रारंभ")

            return True

        except Exception as e:

            print("त्रुटि:", e)

            return False
