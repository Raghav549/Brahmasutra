import os
import zipfile
import subprocess
import random


class सूत्रCreatorAIv25:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v25")

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

<p>सूत्र Creator AI v25 App</p>

<button onclick="run()">Run</button>

<script>
function run()
{{
alert("सूत्र App running successfully");
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


    def launcher(self, root):

        launcher = """
सूत्र Android Launcher

WebView load:
assets/index.html

Display screen

Start app
"""

        open(root+"/launcher.txt","w").write(launcher)


    def apk(self, root, name):

        apk_path = root+"/apk/"+name+".apk"

        zipf = zipfile.ZipFile(apk_path,"w")

        zipf.write(root+"/AndroidManifest.xml","AndroidManifest.xml")
        zipf.write(root+"/launcher.txt","launcher.txt")
        zipf.write(root+"/assets/index.html","assets/index.html")

        zipf.close()

        print("APK निर्मित:", apk_path)

        return apk_path


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

        self.launcher(root)

        apk = self.apk(root,name)

        self.install(apk)

        print("App ready:", name)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, cmd

    print("🕉️ सूत्र Universal Creator AI v25 सक्रिय")


    ai = सूत्रCreatorAIv25()

    while True:

        cmd = input("CreatorAIv25 >>> ")

        if cmd == "निर्गम":
            break

        if cmd.startswith("create"):
            ai.create(cmd)

        else:
            print("Unknown command")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
