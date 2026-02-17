# 🕉️ सूत्र Universal Creator AI v17
# TRUE UNIVERSAL SOFTWARE GENERATOR

import os
import random
import subprocess
import http.server
import socketserver
import threading

print("🕉️ Creator AI v17 सक्रिय")


class CreatorAIv17:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v17")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def generate_name(self,prompt):

        parts = prompt.split()

        if len(parts)>=2:
            return parts[1]

        return "सूत्र_"+str(random.randint(1000,9999))


    def create_structure(self,name):

        root = os.path.join(self.base,name)

        os.makedirs(root,exist_ok=True)

        folders = [

        "frontend",
        "backend",
        "ai",
        "android",
        "automation",
        "database"

        ]

        for f in folders:

            os.makedirs(root+"/"+f,exist_ok=True)

        return root


    def generate_frontend(self,name):

        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffaa;text-align:center">

<h1>{name}</h1>

<input id="input">

<button onclick="run()">Execute</button>

<p id="output"></p>

<script>

function run()
{{
let x=document.getElementById("input").value
document.getElementById("output").innerText="AI:"+x
}}

</script>

</body>
</html>
"""


    def generate_backend(self,name):

        return f"""
print("🕉️ backend active")

def process(x):

    return "processed:"+x
"""


    def generate_ai(self,name):

        return f"""
print("🕉️ AI active")

class AI:

    def run(self,x):

        return "AI processed:"+x
"""


    def generate_android(self,name):

        return f"""
# Android APK Project

app_name="{name}"

print("Android project ready")
"""


    def generate_automation(self,name):

        return f"""
print("automation ready")

def run():

    print("task executed")
"""


    def generate_database(self,name):

        return f"""
database="{name}_db"

print("database ready")
"""


    def generate_main(self,name):

        return f"""
print("🕉️ system started")

print("frontend ok")
print("backend ok")
print("AI ok")
print("android ok")
print("automation ok")
print("database ok")
"""


    def deploy(self,path):

        os.chdir(path+"/frontend")

        PORT=9091

        Handler=http.server.SimpleHTTPRequestHandler

        httpd=socketserver.TCPServer(("",PORT),Handler)

        print("🌐 deployed at port",PORT)

        httpd.serve_forever()


    def deploy_thread(self,path):

        t=threading.Thread(target=self.deploy,args=(path,))

        t.daemon=True

        t.start()


    def run(self,path):

        subprocess.run(["python",path+"/main.py"])


    def build(self,prompt):

        name=self.generate_name(prompt)

        path=self.create_structure(name)

        open(path+"/frontend/index.html","w",encoding="utf-8").write(self.generate_frontend(name))

        open(path+"/backend/server.py","w",encoding="utf-8").write(self.generate_backend(name))

        open(path+"/ai/ai.py","w",encoding="utf-8").write(self.generate_ai(name))

        open(path+"/android/project.py","w",encoding="utf-8").write(self.generate_android(name))

        open(path+"/automation/auto.py","w",encoding="utf-8").write(self.generate_automation(name))

        open(path+"/database/db.py","w",encoding="utf-8").write(self.generate_database(name))

        open(path+"/main.py","w",encoding="utf-8").write(self.generate_main(name))

        print("🕉️ software generated")

        self.run(path)

        self.deploy_thread(path)

        print("🌐 deployed")
        print("location:",path)


# RUN

ai=CreatorAIv17()

while True:

    prompt=input("CreatorAIv17 >>> ")

    if prompt=="निर्गम":
        break

    ai.build(prompt)
