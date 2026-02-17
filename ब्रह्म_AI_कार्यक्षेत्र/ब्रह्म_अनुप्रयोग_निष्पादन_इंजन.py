import os


class ब्रह्मअनुप्रयोगनिष्पादनइंजन:

    def __init__(self):

        self.सक्रिय_अनुप्रयोग = None

        print("ब्रह्म अनुप्रयोग निष्पादन इंजन सक्रिय")


    def निष्पादित(self, path):

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return False


        try:

            with open(path, "r", encoding="utf-8") as file:

                code = file.read()


            namespace = {}

            exec(code, namespace)


            self.सक्रिय_अनुप्रयोग = path

            print(f"अनुप्रयोग निष्पादित: {path}")

            return True


        except Exception as e:

            print("निष्पादन त्रुटि:", e)

            return False


    def सक्रिय(self):

        return self.सक्रिय_अनुप्रयोग


    def बंद(self):

        print("अनुप्रयोग बंद")

        self.सक्रिय_अनुप्रयोग = None
