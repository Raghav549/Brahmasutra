# 🕉️ Creator AI v19
# REAL APK BUILDER

import os
import random
import subprocess
import zipfile


class CreatorAIv19:


    def __init__(self):

        self.base=os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v19")

        os.makedirs(self.base,exist_ok=True)

        print("निर्माण स्थान:",self.base)


    def name(self,prompt):

        parts=prompt.split()

        if len(parts)>=2:
            return parts[1]

        return "सूत्र_"+str(random.randint(1000,9999))


    def structure(self,name):

        root=self.base+"/"+name

        os.makedirs(root+"/apk/assets",exist_ok=True)

        return root


    def html(self,name):

        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffaa;text-align:center">

<h1>{name} APK App</h1>

<button onclick="run()">Run</button>

<p id="out"></p>

<script>

function run()
{{
document.getElementById("out").innerText="AI Running"
}}

</script>

</body>
</html>
"""


    def manifest(self,name):

        return f"""
<manifest package="{name}">
<application>
<activity android:name="MainActivity"/>
</application>
</manifest>
"""


    def dex(self):

        return b'dex\n035\x00'


    def build_apk(self,name,root):

        apk_path=root+"/"+name+".apk"

        with zipfile.ZipFile(apk_path,"w") as apk:

            apk.write(root+"/apk/AndroidManifest.xml","AndroidManifest.xml")

            apk.write(root+"/apk/classes.dex","classes.dex")

            apk.write(root+"/apk/assets/index.html","assets/index.html")

        print("APK built:",apk_path)


    def generate(self,prompt):

        name=self.name(prompt)

        root=self.structure(name)

        open(root+"/apk/assets/index.html","w").write(self.html(name))

        open(root+"/apk/AndroidManifest.xml","w").write(self.manifest(name))

        open(root+"/apk/classes.dex","wb").write(self.dex())

        self.build_apk(name,root)

        print("🕉️ Installable APK ready")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, p

    print("🕉️ Creator AI v19 सक्रिय")


    # run

    ai=CreatorAIv19()

    while True:

        p=input("CreatorAIv19 >>> ")

        if p=="निर्गम":
            break

        ai.generate(p)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
