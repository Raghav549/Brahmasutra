import os
import zipfile
import random


class सूत्रAPKनिर्माता:


    def __init__(self):

        print("🕉️ सूत्र APK निर्माता सक्रिय")

        self.output = "निर्मित_APK"

        if not os.path.exists(self.output):

            os.mkdir(self.output)


    def नाम(self):

        return "सूत्रAPK" + str(random.randint(1000,9999))


    def manifest(self, नाम, path):

        content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest package="{नाम}">
<application label="{नाम}">
<activity name="MainActivity"/>
</application>
</manifest>
"""

        with open(path+"/AndroidManifest.xml","w") as f:

            f.write(content)


    def dex(self, path):

        dex_data = b"SUTRADEX"

        with open(path+"/classes.dex","wb") as f:

            f.write(dex_data)


    def apk_zip(self, folder, apk_name):

        apk_path = self.output + "/" + apk_name + ".apk"

        with zipfile.ZipFile(apk_path, 'w') as apk:

            for root, dirs, files in os.walk(folder):

                for file in files:

                    full = os.path.join(root,file)

                    rel = os.path.relpath(full,folder)

                    apk.write(full, rel)

        print("APK निर्मित:", apk_path)


    def निर्माण(self):

        नाम = self.नाम()

        temp = "temp_apk"

        if not os.path.exists(temp):

            os.mkdir(temp)


        self.manifest(नाम, temp)

        self.dex(temp)

        self.apk_zip(temp, नाम)
