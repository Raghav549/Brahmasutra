# 🕉️ ब्रह्म AI एकल अनुप्रयोग निर्माता VERSION 36

import os
import re

class ब्रह्मएकलअनुप्रयोगनिर्माता:

    def __init__(self):
        print("🕉️ ब्रह्म एकल अनुप्रयोग निर्माता सक्रिय")

        self.root = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_एकल_अनुप्रयोग"
        )

        os.makedirs(self.root, exist_ok=True)

    # prompt → safe app name
    def नाम_निर्माण(self, prompt):

        name = prompt.lower()

        name = re.sub(r'[^a-z0-9 ]', '', name)

        name = name.strip().replace(" ", "_")

        if len(name) == 0:
            name = "brahma_app"

        return name

    # main generator
    def निर्मित(self, prompt):

        app_name = self.नाम_निर्माण(prompt)

        app_path = os.path.join(self.root, app_name)

        if os.path.exists(app_path):
            print("अनुप्रयोग पहले से मौजूद:", app_name)
            return app_path

        print("अनुप्रयोग निर्माण प्रारम्भ:", app_name)

        # create folders
        os.makedirs(app_path)
        os.makedirs(app_path + "/frontend")
        os.makedirs(app_path + "/backend")
        os.makedirs(app_path + "/database")

        # create frontend
        self.फ्रंटएंड(app_path, prompt)

        # create backend
        self.बैकएंड(app_path, prompt)

        # create database
        self.डेटाबेस(app_path)

        print("✅ पूर्ण अनुप्रयोग निर्मित:", app_path)

        return app_path

    def फ्रंटएंड(self, app_path, prompt):

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{prompt}</title>
</head>

<body>

<h1>BRAHMA AI GENERATED APP</h1>

<p>Prompt: {prompt}</p>

<button onclick="test()">Test Backend</button>

<p id="output"></p>

<script>

function test()
{{
fetch("http://127.0.0.1:5000/api")
.then(r=>r.json())
.then(d=>{{
document.getElementById("output").innerText =
JSON.stringify(d)
}})
}}

</script>

</body>
</html>
"""

        with open(app_path + "/frontend/index.html", "w") as f:
            f.write(html)

    def बैकएंड(self, app_path, prompt):

        code = f'''
# 🕉️ BRAHMA AI BACKEND

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api")
def api():

    return jsonify({{
        "status":"ok",
        "app":"{prompt}",
        "engine":"BRAHMA AI VERSION 36"
    }})

if __name__ == "__main__":
    app.run(port=5000)
'''

        with open(app_path + "/backend/api.py", "w") as f:
            f.write(code)

    def डेटाबेस(self, app_path):

        db = """
-- BRAHMA AI DATABASE

CREATE TABLE users(
id INTEGER PRIMARY KEY,
username TEXT,
password TEXT
);
"""

        with open(app_path + "/database/schema.sql", "w") as f:
            f.write(db)
