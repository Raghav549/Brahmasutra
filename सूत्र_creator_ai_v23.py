import os
import random
import zipfile
import subprocess

class सूत्रCreatorAIv23:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v23")
        os.makedirs(self.base, exist_ok=True)

        print("निर्माण पथ:", self.base)


    def नाम_निकालो(self, prompt):

        words = prompt.split()

        if len(words) >= 2:
            return words[1]

        return "app_" + str(random.randint(1000,9999))


    def project_निर्माण(self, name):

        root = os.path.join(self.base,name)

        os.makedirs(root+"/apk", exist_ok=True)
        os.makedirs(root+"/android/assets", exist_ok=True)
        os.makedirs(root+"/android/res", exist_ok=True)

        return root


    def gui_निर्माण(self, root, name):

        html = root+"/android/assets/index.html"

        data = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>

<style>

body {{
background:black;
color:cyan;
font-family:sans-serif;
text-align:center;
margin-top:100px;
}}

button {{
padding:20px;
font-size:20px;
background:cyan;
color:black;
border:none;
}}

</style>

</head>

<body>

<h1>🕉️ {name} App</h1>

<p>सूत्र Creator AI v23 द्वारा निर्मित</p>

<button onclick="run()">Start</button>

<script>

function run() {{
alert("सूत्र App सक्रिय");
}}

</script>

</body>

</html>
"""

        with open(html,"w",encoding="utf-8") as f:
            f.write(data)

        return html


    def manifest_निर्माण(self, root, name):

        manifest = root+"/android/AndroidManifest.xml"

        data = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.{name}">

<application
android:label="{name}"
android:icon="@android:drawable/sym_def_app_icon">

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


    def launcher_निर्माण(self, root):

        launcher = root+"/android/MainActivity.txt"

        data = """
सूत्र Android Launcher
App प्रारम्भ
GUI load
assets/index.html
"""

        with open(launcher,"w") as f:
            f.write(data)


    def apk_निर्माण(self, root, name):

        apk = root+"/apk/"+name+".apk"

        zipf = zipfile.ZipFile(apk,"w")

        zipf.write(root+"/android/assets/index.html","assets/index.html")
        zipf.write(root+"/android/AndroidManifest.xml","AndroidManifest.xml")
        zipf.write(root+"/android/MainActivity.txt","MainActivity.txt")

        zipf.close()

        print("Installable APK निर्मित:", apk)

        return apk


    def install(self, apk):

        try:

            subprocess.run(["termux-open", apk])
            print("Install dialog opened")

        except:

            print("Manual install:", apk)


    def create(self, prompt):

        name = self.नाम_निकालो(prompt)

        root = self.project_निर्माण(name)

        self.gui_निर्माण(root,name)

        self.manifest_निर्माण(root,name)

        self.launcher_निर्माण(root)

        apk = self.apk_निर्माण(root,name)

        self.install(apk)

        print("पूर्ण App निर्माण:", root)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, cmd

    print("🕉️ सूत्र Universal Creator AI v23 सक्रिय")


    ai = सूत्रCreatorAIv23()

    while True:

        cmd = input("CreatorAIv23 >>> ")

        if cmd == "निर्गम":
            break

        if cmd.startswith("create") or cmd.startswith("app") or cmd.startswith("website"):

            ai.create(cmd)

        else:

            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
