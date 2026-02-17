# 🕉️ सूत्र Universal Creator AI v13
# PROMPT → FULL PROJECT GENERATOR

import os
import datetime

print("🕉️ सूत्र Creator AI v13 सक्रिय")


class सूत्रCreatorAI:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v13")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def project_name(self, prompt):

        parts = prompt.split()

        if len(parts) >= 2:
            return parts[1]

        return "सूत्रProject"


    def create_structure(self, name):

        path = os.path.join(self.base, name)

        os.makedirs(path, exist_ok=True)

        os.makedirs(path+"/frontend", exist_ok=True)
        os.makedirs(path+"/backend", exist_ok=True)
        os.makedirs(path+"/database", exist_ok=True)
        os.makedirs(path+"/ai", exist_ok=True)

        return path


    def create_website(self, name):

        path = self.create_structure(name)

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>

<body style="background:black;color:#00ffcc;text-align:center;">

<h1>{name}</h1>

<p>सूत्र Creator AI v13 द्वारा निर्मित</p>

<button onclick="run()">Run</button>

<script>

function run()
{{

alert("सूत्र सक्रिय")

}}

</script>

</body>
</html>
"""

        with open(path+"/frontend/index.html","w",encoding="utf-8") as f:

            f.write(html)

        print("Website ready:", path)


    def create_backend(self, name):

        path = os.path.join(self.base,name+"/backend")

        code = f"""
print("🕉️ {name} Backend Server")

while True:

    cmd = input("server> ")

    if cmd == "exit":
        break

    print("processing:",cmd)
"""

        with open(path+"/server.py","w",encoding="utf-8") as f:

            f.write(code)


    def create_ai(self,name):

        path = os.path.join(self.base,name+"/ai")

        code = f"""
print("🕉️ {name} AI Module")

def run(prompt):

    print("AI processing:",prompt)
"""

        with open(path+"/ai.py","w",encoding="utf-8") as f:

            f.write(code)


    def create_database(self,name):

        path = os.path.join(self.base,name+"/database")

        code = f"""
data = {{}}

def save(k,v):

    data[k]=v

def load(k):

    return data.get(k)
"""

        with open(path+"/db.py","w",encoding="utf-8") as f:

            f.write(code)


    def create_main(self,name):

        path = os.path.join(self.base,name)

        code = f"""
print("🕉️ {name} Software प्रारम्भ")

print("Frontend ready")
print("Backend ready")
print("AI ready")
print("Database ready")
"""

        with open(path+"/main.py","w",encoding="utf-8") as f:

            f.write(code)


    def build(self,prompt):

        name = self.project_name(prompt)

        self.create_website(name)

        self.create_backend(name)

        self.create_ai(name)

        self.create_database(name)

        self.create_main(name)

        print("Full Project ready:",name)


# START

ai = सूत्रCreatorAI()

while True:

    prompt = input("CreatorAIv13 >>> ")

    if prompt == "निर्गम":
        break

    ai.build(prompt)
