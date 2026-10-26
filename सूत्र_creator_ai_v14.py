# 🕉️ सूत्र Universal Creator AI v14
# SELF GENERATING SOFTWARE AI

import os
import datetime
import random


class CreatorAIv14:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v14")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण स्थान:", self.base)


    def generate_name(self, prompt):

        parts = prompt.split()

        if len(parts) >= 2:

            return parts[1]

        return "सूत्रAI_"+str(random.randint(1000,9999))


    def generate_ui(self, name):

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

let v = document.getElementById("input").value

document.getElementById("output").innerText="Output: "+v

}}

</script>

</body>
</html>
"""

        return html


    def generate_backend(self, name):

        code = f"""
print("🕉️ {name} Backend Active")

while True:

    cmd = input("server> ")

    if cmd=="exit":
        break

    print("processed:",cmd)
"""

        return code


    def generate_ai(self,name):

        code = f"""
print("🕉️ {name} AI Active")

def think(prompt):

    return "AI response: "+prompt
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


    def generate_main(self,name):

        code = f"""
print("🕉️ {name} Software Active")

print("UI ready")
print("Backend ready")
print("AI ready")
print("Database ready")
"""

        return code


    def build(self,prompt):

        name = self.generate_name(prompt)

        path = os.path.join(self.base,name)

        os.makedirs(path, exist_ok=True)

        os.makedirs(path+"/frontend", exist_ok=True)
        os.makedirs(path+"/backend", exist_ok=True)
        os.makedirs(path+"/ai", exist_ok=True)
        os.makedirs(path+"/database", exist_ok=True)

        with open(path+"/frontend/index.html","w",encoding="utf-8") as f:

            f.write(self.generate_ui(name))

        with open(path+"/backend/server.py","w",encoding="utf-8") as f:

            f.write(self.generate_backend(name))

        with open(path+"/ai/ai.py","w",encoding="utf-8") as f:

            f.write(self.generate_ai(name))

        with open(path+"/database/db.py","w",encoding="utf-8") as f:

            f.write(self.generate_db(name))

        with open(path+"/main.py","w",encoding="utf-8") as f:

            f.write(self.generate_main(name))

        print("Full AI Software Generated:",name)

        print("Location:",path)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, prompt

    print("🕉️ सूत्र Creator AI v14 सक्रिय")


    # RUN

    ai = CreatorAIv14()

    while True:

        prompt = input("CreatorAIv14 >>> ")

        if prompt=="निर्गम":

            break

        ai.build(prompt)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
