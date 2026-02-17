# 🕉️ सूत्र Application Runtime Engine


import os

from सूत्र_NATIVE_EXECUTION import NativeExecutor


class Runtime:


    def __init__(self):

        print("🕉️ सूत्र Application Runtime सक्रिय")

        self.executor = NativeExecutor()


    def चलाओ(self, app_path):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")

            return


        print("अनुप्रयोग प्रारम्भ:", app_path)


        self.executor.निष्पादन(app_path)


        print("अनुप्रयोग समाप्त")
