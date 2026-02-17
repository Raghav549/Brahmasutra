import os
import zipfile
import subprocess
import random
import time

print("🕉️ सूत्र Universal Creator AI v26 सक्रिय")


class सूत्रCreatorAIv26:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v26")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def नाम(self, prompt):

        parts = prompt.split()

        if len(parts) >= 2:
            return parts[1]

        return "app_"+str(random.randint(1000,9999))


    def संरचना(self, name):

        root = self.base+"/"+name

        os.makedirs(root+"/assets", exist_ok=True)
        os.makedirs(root+"/res", exist_ok=True)
        os.makedirs(root+"/META-INF", exist_ok=True)
        os.makedirs(root+"/apk", exist_ok=True)

        return root


    def html(self, root, name):

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
<style>
body {{
background:black;
color:#00ffd5;
text-align:center;
font-size:28px;
margin-top:200px;
}}
</style>
</head>
<body>

🕉️ {name} App running

<script>

document.body.onclick = function()
{{
alert("सूत्र Creator AI v26 App running");
}}

</script>

</body>
</html>
"""

        open(root+"/assets/index.html","w").write(html)


    def manifest(self, root, name):

        manifest = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.{name}">

<application
android:label="{name}"
android:icon="@android:drawable/sym_def_app_icon">

<activity android:name="Main">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>
"""

        open(root+"/AndroidManifest.xml","w").write(manifest)


    def meta(self, root):

        open(root+"/META-INF/MANIFEST.MF","w").write("Manifest-Version: 1.0")
        open(root+"/META-INF/CERT.SF","w").write("Signature-Version: 1.0")
        open(root+"/META-INF/CERT.RSA","w").write("RSA")


    def classes(self, root):

        open(root+"/classes.dex","w").write("सूत्र dex")


    def apk(self, root, name):

        apk = root+"/apk/"+name+".apk"

        z = zipfile.ZipFile(apk,"w")

        z.write(root+"/AndroidManifest.xml","AndroidManifest.xml")
        z.write(root+"/classes.dex","classes.dex")

        z.write(root+"/META-INF/MANIFEST.MF","META-INF/MANIFEST.MF")
        z.write(root+"/META-INF/CERT.SF","META-INF/CERT.SF")
        z.write(root+"/META-INF/CERT.RSA","META-INF/CERT.RSA")

        z.write(root+"/assets/index.html","assets/index.html")

        z.close()

        print("APK निर्मित:", apk)

        return apk


    def install(self, apk):

        try:

            subprocess.run(["termux-open", apk])
            print("Install dialog opened")

        except:

            print("Manual install:", apk)


    def create(self, prompt):

        name = self.नाम(prompt)

        root = self.संरचना(name)

        self.html(root,name)

        self.manifest(root,name)

        self.meta(root)

        self.classes(root)

        apk = self.apk(root,name)

        time.sleep(1)

        self.install(apk)

        print("App ready:", name)


ai = सूत्रCreatorAIv26()

while True:

    cmd = input("CreatorAIv26 >>> ")

    if cmd == "निर्गम":
        break

    if cmd.startswith("create"):
        ai.create(cmd)

    else:
        print("Unknown command")
