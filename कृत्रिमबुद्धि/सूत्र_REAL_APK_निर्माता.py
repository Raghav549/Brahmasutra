import os
import zipfile
import random


class सूत्रREALAPKनिर्माता:


    def __init__(self):

        print("🕉️ सूत्र REAL APK निर्माता सक्रिय")

        self.output = "REAL_APK"

        if not os.path.exists(self.output):

            os.mkdir(self.output)


    def नाम(self):

        return "सूत्रREAL" + str(random.randint(1000,9999))


    def manifest(self, नाम, path):

        content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="{नाम}">

<application
android:label="सूत्र OS"
android:theme="@android:style/Theme.DeviceDefault">

<activity
android:name="MainActivity"
android:exported="true">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>
"""

        with open(path+"/AndroidManifest.xml","w") as f:

            f.write(content)


    def dex(self, path):

        data = b"dex\n035\0SUTRAREAL"

        with open(path+"/classes.dex","wb") as f:

            f.write(data)


    def resources(self, path):

        os.mkdir(path+"/res")


    def apk_zip(self, folder, apk_name):

        apk_path = self.output + "/" + apk_name + ".apk"

        with zipfile.ZipFile(apk_path, 'w') as apk:

            for root, dirs, files in os.walk(folder):

                for file in files:

                    full = os.path.join(root,file)

                    rel = os.path.relpath(full,folder)

                    apk.write(full, rel)

        print("REAL APK निर्मित:", apk_path)


    def निर्माण(self):

        नाम = self.नाम()

        temp = "temp_real_apk"

        if not os.path.exists(temp):

            os.mkdir(temp)


        self.manifest(नाम, temp)

        self.dex(temp)

        self.resources(temp)

        self.apk_zip(temp, नाम)
