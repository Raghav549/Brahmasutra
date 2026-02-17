import os
from सूत्र_कार्य_निष्पादक import कार्यनिष्पादक

class यन्त्रलोडर:

    def __init__(self):

        print("🕉️ सूत्र यन्त्र लोडर सक्रिय")

        self.executor = कार्यनिष्पादक()

        self.temp_dir = os.path.expanduser("~/सूत्र-तंत्र/temp")

        if not os.path.exists(self.temp_dir):

            os.makedirs(self.temp_dir)


    def निष्पादन(self, path):

        print("यन्त्र लोड हो रहा है:", path)

        if not os.path.exists(path):

            print("त्रुटि: यन्त्र नहीं मिला")

            return


        with open(path, "r", encoding="utf-8") as f:

            data = f.read()


        temp_file = os.path.join(self.temp_dir, "temp.कार्य")


        with open(temp_file, "w", encoding="utf-8") as f:

            f.write(data)


        print("यन्त्र निष्पादन प्रारम्भ")

        self.executor.निष्पादन(temp_file)
