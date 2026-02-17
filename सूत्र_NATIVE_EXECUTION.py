# 🕉️ सूत्र Native Execution Engine


import os


class NativeExecutor:


    def __init__(self):

        print("🕉️ सूत्र Native Execution Engine सक्रिय")


    def निष्पादन(self, पथ):

        if not os.path.exists(पथ):

            print("त्रुटि: binary नहीं मिला")

            return


        print("Native binary लोड:", पथ)


        with open(पथ,"r",encoding="utf-8") as f:

            code = f.read()


        self.चलाओ(code)


    def चलाओ(self, code):

        पंक्तियाँ = code.splitlines()


        for पंक्ति in पंक्तियाँ:

            पंक्ति = पंक्ति.strip()


            if पंक्ति.startswith("स्थापित"):

                print("Execute:", पंक्ति)


            elif पंक्ति.startswith("योग"):

                print("Execute:", पंक्ति)


            elif पंक्ति.startswith("दर्शय"):

                print("Execute:", पंक्ति)


            elif पंक्ति.startswith("निर्गम"):

                print("Program समाप्त")

                break
