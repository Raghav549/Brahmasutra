import os
import random
import zipfile
import subprocess

print("🕉️ सूत्र Universal Creator AI v22 सक्रिय")

class सूत्रCreatorAIv22:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v22")
        os.makedirs(self.base, exist_ok=True)

        print("निर्माण पथ:", self.base)


    def नाम_निकालो(self, prompt):

        words = prompt.split()

        if len(words) >= 2:
            return words[1]

        return "app_" + str(random.randint(1000,9999))


    def project_निर्माण(self, name):

        root = os.path.join(self.base,name)

        os.makedirs(root, exist_ok=True)
        os.makedirs(root+"/apk", exist_ok=True)
        os.makedirs(root+"/website", exist_ok=True)
        os.makedirs(root+"/android/assets", exist_ok=True)

        return root


    def website_निर्माण(self, root, name):

        html = root+"/website/index.html"

        data = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>
<body>
<h1>🕉️ {name} App</h1>
<p>सूत्र Creator AI v22 द्वारा निर्मित</p>
</body>
</html>
"""

        with open(html,"w",encoding="utf-8") as f:
            f.write(data)

        return html


    def manifest_निर्माण(self, root):

        manifest = root+"/android/AndroidManifest.xml"

        data = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.app">

<application android:label="Sutra App">

<activity android:name=".MainActivity">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>
<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>
"""

        with open(manifest,"w") as f:
            f.write(data)


    def apk_निर्माण(self, root, name):

        apk_path = root+"/apk/"+name+".apk"

        zipf = zipfile.ZipFile(apk_path,"w")

        zipf.write(root+"/website/index.html","assets/index.html")
        zipf.write(root+"/android/AndroidManifest.xml","AndroidManifest.xml")

        zipf.close()

        print("Installable APK निर्मित:", apk_path)

        return apk_path


    def install(self, apk):

        try:

            subprocess.run(["termux-open", apk])

            print("Install dialog opened")

        except:

            print("Manual install:", apk)


    def create(self, prompt):

        name = self.नाम_निकालो(prompt)

        root = self.project_निर्माण(name)

        html = self.website_निर्माण(root,name)

        self.manifest_निर्माण(root)

        apk = self.apk_निर्माण(root,name)

        self.install(apk)

        print("पूर्ण निर्माण:", root)


ai = सूत्रCreatorAIv22()

while True:

    cmd = input("CreatorAIv22 >>> ")

    if cmd == "निर्गम":
        break

    if cmd.startswith("create") or cmd.startswith("app") or cmd.startswith("website"):

        ai.create(cmd)

    else:

        print("अज्ञात आदेश")
