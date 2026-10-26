# 🕉️ सूत्र Creator AI v18
# REAL APK + REAL SAAS GENERATOR

import os
import random
import subprocess
import sys
import threading
import http.server
import socketserver


class CreatorAIv18:


    def __init__(self):

        self.base=os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v18")

        os.makedirs(self.base,exist_ok=True)

        print("निर्माण स्थान:",self.base)


    def name(self,prompt):

        parts=prompt.split()

        if len(parts)>=2:
            return parts[1]

        return "सूत्र_"+str(random.randint(1000,9999))


    def structure(self,name):

        root=self.base+"/"+name

        folders=[

        "frontend",
        "backend",
        "android",
        "ai",
        "database",
        "build"

        ]

        for f in folders:

            os.makedirs(root+"/"+f,exist_ok=True)

        return root


    def frontend(self,name):

        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffaa;text-align:center">

<h1>{name} AI System</h1>

<input id="input">

<button onclick="run()">Run</button>

<p id="output"></p>

<script>

function run()
{{
let x=document.getElementById("input").value
document.getElementById("output").innerText="Processed:"+x
}}

</script>

</body>
</html>
"""


    def backend(self):

        return """
print("🕉️ backend running")

def process(x):

    return "processed:"+x
"""


    def ai(self):

        return """
print("🕉️ AI ready")

class AI:

    def execute(self,x):

        return "AI:"+x
"""


    def database(self,name):

        return f"""
database="{name}"

print("database ready")
"""


    def android_manifest(self,name):

        return f"""
<manifest package="{name}">
<application>
<activity android:name="MainActivity"/>
</application>
</manifest>
"""


    def android_main(self,name):

        return f"""
package {name};

public class MainActivity
{{
public static void main(String[] args)
{{
System.out.println("AI App Running");
}}
}}
"""


    def build_script(self,name):

        return f"""
echo Building APK project {name}
"""


    def main(self):

        return """
print("system active")
"""


    def deploy(self,path):

        os.chdir(path+"/frontend")

        Handler=http.server.SimpleHTTPRequestHandler

        httpd=socketserver.TCPServer(("",9092),Handler)

        print("🌐 deployed at http://localhost:9092")

        httpd.serve_forever()


    def deploy_thread(self,path):

        t=threading.Thread(target=self.deploy,args=(path,))
        t.daemon=True
        t.start()


    def generate(self,prompt):

        name=self.name(prompt)

        root=self.structure(name)

        open(root+"/frontend/index.html","w").write(self.frontend(name))

        open(root+"/backend/server.py","w").write(self.backend())

        open(root+"/ai/ai.py","w").write(self.ai())

        open(root+"/database/db.py","w").write(self.database(name))

        open(root+"/android/AndroidManifest.xml","w").write(self.android_manifest(name))

        open(root+"/android/MainActivity.java","w").write(self.android_main(name))

        open(root+"/build/build.sh","w").write(self.build_script(name))

        open(root+"/main.py","w").write(self.main())

        print("🕉️ Full software generated")

        subprocess.run([sys.executable,root+"/main.py"])

        self.deploy_thread(root)

        print("APK project ready")
        print("Location:",root)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, p


    print("🕉️ Creator AI v18 सक्रिय")


    # run

    ai=CreatorAIv18()

    while True:

        p=input("CreatorAIv18 >>> ")

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
