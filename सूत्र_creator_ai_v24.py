import os
import zipfile
import random
import subprocess

print("🕉️ सूत्र Universal Creator AI v24 सक्रिय")

class सूत्रCreatorAIv24:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v24")
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
        os.makedirs(root+"/apk", exist_ok=True)

        return root


    def gui(self, root, name):

        file = root+"/assets/index.html"

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
font-family:sans-serif;
margin-top:150px;
}}

button {{
padding:20px;
font-size:22px;
background:#00ffd5;
color:black;
border:none;
}}

</style>

</head>

<body>

<h1>🕉️ {name}</h1>

<p>सूत्र Creator AI v24 App</p>

<button onclick="start()">Start</button>

<script>

function start()
{{
alert("सूत्र App running");
}}

</script>

</body>

</html>
"""

        open(file,"w").write(html)


    def manifest(self, root, name):

        data = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.{name}">

<application
android:label="{name}"
android:theme="@android:style/Theme.DeviceDefault.Light">

<activity android:name=".Main">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>
"""

        open(root+"/AndroidManifest.xml","w").write(data)


    def launcher(self, root):

        code = """
सूत्र Launcher

Load GUI
assets/index.html

Display GUI
"""

        open(root+"/Main.txt","w").write(code)


    def apk(self, root, name):

        apkfile = root+"/apk/"+name+".apk"

        zipf = zipfile.ZipFile(apkfile,"w")

        zipf.write(root+"/AndroidManifest.xml","AndroidManifest.xml")

        zipf.write(root+"/Main.txt","Main.txt")

        zipf.write(root+"/assets/index.html","assets/index.html")

        zipf.close()

        print("APK ready:", apkfile)

        return apkfile


    def install(self, apk):

        try:

            subprocess.run(["termux-open", apk])

            print("Install dialog opened")

        except:

            print("Manual install:", apk)


    def create(self, prompt):

        name = self.नाम(prompt)

        root = self.संरचना(name)

        self.gui(root,name)

        self.manifest(root,name)

        self.launcher(root)

        apk = self.apk(root,name)

        self.install(apk)

        print("App created:", name)


ai = सूत्रCreatorAIv24()

while True:

    cmd = input("CreatorAIv24 >>> ")

    if cmd == "निर्गम":

        break

    if cmd.startswith("create"):

        ai.create(cmd)

    else:

        print("Unknown command")
