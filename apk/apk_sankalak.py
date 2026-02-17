import os
import zipfile

class सूत्रAPKSंकलक:

    def __init__(self):

        self.परियोजना = os.path.expanduser("~/सूत्र-तंत्र/apk/सूत्रApp")

        self.apk = os.path.expanduser("~/सूत्र-तंत्र/सूत्रOS.apk")


    def संकलन(self):

        print("APK संकलन प्रारम्भ")

        with zipfile.ZipFile(self.apk, 'w') as apk:

            for root, dirs, files in os.walk(self.परियोजना):

                for file in files:

                    path = os.path.join(root, file)

                    apk.write(path)

        print("APK सफलतया निर्मित")

        print("स्थान:", self.apk)
