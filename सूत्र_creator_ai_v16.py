# 🕉️ सूत्र Universal Creator AI v16
# DEPLOYMENT LEVEL AUTONOMOUS CREATOR

import os
import random
import subprocess
import http.server
import socketserver
import threading

print("🕉️ सूत्र Creator AI v16 सक्रिय")


class CreatorAIv16:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v16")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def generate_name(self, prompt):

        parts = prompt.split()

        if len(parts)>=2:

            return parts[1]

        return "सूत्रAI_"+str(random.randint(1000,9999))


    def create_structure(self,name):

        path = os.path.join(self.base,name)

        os.makedirs(path,exist_ok=True)

        os.makedirs(path+"/frontend",exist_ok=True)
        os.makedirs(path+"/backend",exist_ok=True)
        os.makedirs(path+"/ai",exist_ok=True)

        return path


    def generate_frontend(self,name):

        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffcc;text-align:center;">

<h1>{name}</h1>

<input id="input">

<button onclick="send()">Run</button>

<p id="out"></p>

<script>

function send()
{{

let v=document.getElementById("input").value

document.getElementById("out").innerText="AI running:"+v

}}

</script>

</body>
</html>
"""


    def generate_backend(self,name):

        return f"""
print("🕉️ {name} backend active")

def run(x):

    return "processed:"+x
"""


    def generate_ai(self,name):

        return f"""
print("🕉️ {name} AI active")

class AI:

    def process(self,x):

        return "AI:"+x
"""


    def generate_main(self,name):

        return f"""
print("🕉️ {name} system started")

print("frontend ready")
print("backend ready")
print("AI ready")
"""


    def deploy_server(self,path):

        os.chdir(path+"/frontend")

        PORT = 9090

        Handler = http.server.SimpleHTTPRequestHandler

        httpd = socketserver.TCPServer(("", PORT), Handler)

        print("🌐 server running on port",PORT)

        httpd.serve_forever()


    def start_server_thread(self,path):

        t = threading.Thread(target=self.deploy_server,args=(path,))

        t.daemon=True

        t.start()


    def run_software(self,path,name):

        print("▶ running software")

        subprocess.run(["python",path+"/main.py"])


    def build(self,prompt):

        name = self.generate_name(prompt)

        path = self.create_structure(name)

        open(path+"/frontend/index.html","w",encoding="utf-8").write(self.generate_frontend(name))

        open(path+"/backend/server.py","w",encoding="utf-8").write(self.generate_backend(name))

        open(path+"/ai/ai.py","w",encoding="utf-8").write(self.generate_ai(name))

        open(path+"/main.py","w",encoding="utf-8").write(self.generate_main(name))

        print("🕉️ software generated")

        self.run_software(path,name)

        self.start_server_thread(path)

        print("🌐 deployed")

        print("location:",path)


# RUN

ai = CreatorAIv16()

while True:

    prompt = input("CreatorAIv16 >>> ")

    if prompt == "निर्गम":

        break

    ai.build(prompt)
