# 🕉️ सूत्र Universal Creator AI v15
# AUTONOMOUS SOFTWARE CREATOR CORE

import os
import random
import datetime

print("🕉️ सूत्र Creator AI v15 सक्रिय")


class CreatorAIv15:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v15")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def generate_name(self, prompt):

        words = prompt.split()

        if len(words) >= 2:

            return words[1]

        return "सूत्रAI_"+str(random.randint(1000,9999))


    def create_structure(self, name):

        path = os.path.join(self.base,name)

        os.makedirs(path, exist_ok=True)

        os.makedirs(path+"/frontend", exist_ok=True)
        os.makedirs(path+"/backend", exist_ok=True)
        os.makedirs(path+"/ai", exist_ok=True)
        os.makedirs(path+"/database", exist_ok=True)
        os.makedirs(path+"/core", exist_ok=True)

        return path


    def generate_frontend(self,name):

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffcc;text-align:center;">

<h1>{name}</h1>

<input id="input">

<button onclick="run()">Run</button>

<p id="output"></p>

<script>

function run()
{{

let v=document.getElementById("input").value

document.getElementById("output").innerText="AI: "+v

}}

</script>

</body>
</html>
"""

        return html


    def generate_backend(self,name):

        code = f"""
print("🕉️ {name} Backend Active")

def run(cmd):

    return "processed:"+cmd
"""

        return code


    def generate_ai(self,name):

        code = f"""
print("🕉️ {name} AI Active")

class AI:

    def think(self,prompt):

        return "AI thinks:"+prompt
"""

        return code


    def generate_db(self,name):

        code = """
db={}

def save(k,v):

    db[k]=v

def load(k):

    return db.get(k)
"""

        return code


    def generate_core(self,name):

        code = f"""
print("🕉️ {name} Core Active")

class Core:

    def start(self):

        print("Core running")
"""

        return code


    def generate_main(self,name):

        code = f"""
print("🕉️ {name} Software Started")

print("Frontend ready")
print("Backend ready")
print("AI ready")
print("Database ready")
print("Core ready")
"""

        return code


    def generate_self_upgrade(self,name,path):

        upgrade = f"""
print("🕉️ {name} Self Upgrade Active")

version = 1

def upgrade():

    global version

    version += 1

    print("Upgraded to version",version)
"""

        with open(path+"/self_upgrade.py","w",encoding="utf-8") as f:

            f.write(upgrade)


    def build(self,prompt):

        name = self.generate_name(prompt)

        path = self.create_structure(name)

        with open(path+"/frontend/index.html","w",encoding="utf-8") as f:

            f.write(self.generate_frontend(name))

        with open(path+"/backend/server.py","w",encoding="utf-8") as f:

            f.write(self.generate_backend(name))

        with open(path+"/ai/ai.py","w",encoding="utf-8") as f:

            f.write(self.generate_ai(name))

        with open(path+"/database/db.py","w",encoding="utf-8") as f:

            f.write(self.generate_db(name))

        with open(path+"/core/core.py","w",encoding="utf-8") as f:

            f.write(self.generate_core(name))

        with open(path+"/main.py","w",encoding="utf-8") as f:

            f.write(self.generate_main(name))

        self.generate_self_upgrade(name,path)

        print("🕉️ Full Autonomous Software Generated")

        print("नाम:",name)

        print("स्थान:",path)


# RUN

ai = CreatorAIv15()

while True:

    prompt = input("CreatorAIv15 >>> ")

    if prompt == "निर्गम":

        break

    ai.build(prompt)
