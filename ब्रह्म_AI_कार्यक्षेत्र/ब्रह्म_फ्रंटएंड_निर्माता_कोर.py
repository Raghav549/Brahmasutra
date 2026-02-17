# 🕉️ BRAHMA FRONTEND GENERATOR ENGINE
# VERSION 112
# FULL SANSKRIT FRONTEND GENERATOR

import os
import json

print("🕉️ ब्रह्म फ्रंटएंड निर्माता कोर सक्रिय (VERSION 112)")


class ब्रह्मफ्रंटएंडनिर्माताकोर:

    def __init__(self):

        self.base_path = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/ब्रह्म_अनुप्रयोग"
        )


    # blueprint load
    def रूपरेखा_लोड(self, app_name):

        blueprint_path = os.path.join(
            self.base_path,
            app_name,
            "config",
            "brahma_blueprint.json"
        )

        if not os.path.exists(blueprint_path):

            print("त्रुटि: blueprint नहीं मिला")
            return None

        with open(blueprint_path, "r", encoding="utf-8") as f:

            return json.load(f)


    # HTML generator
    def HTML_कोड(self, app_name):

        code = f'''
<!DOCTYPE html>
<html>

<head>

<title>{app_name}</title>

<style>

body {{
    font-family: Arial;
    background: #0f172a;
    color: white;
    text-align: center;
}}

button {{
    padding: 12px;
    margin: 10px;
    background: #22c55e;
    border: none;
    color: white;
    cursor: pointer;
}}

input {{
    padding: 10px;
    margin: 10px;
}}

</style>

</head>

<body>

<h1>🕉️ BRAHMA APP: {app_name}</h1>

<h2>Login</h2>

<input id="user" placeholder="Username">
<br>

<input id="pass" placeholder="Password" type="password">
<br>

<button onclick="login()">Login</button>

<h2>Dashboard</h2>

<button onclick="test()">Test Backend</button>

<p id="result"></p>

<script>

function login(){{

    document.getElementById("result").innerText =
    "Login Success (Demo)"

}}

function test(){{

fetch("http://127.0.0.1:8000")

.then(res=>res.json())

.then(data=>{{
document.getElementById("result").innerText =
JSON.stringify(data)
}})

}}

</script>

</body>

</html>
'''

        return code


    # frontend generate
    def निर्माण(self, app_name):

        blueprint = self.रूपरेखा_लोड(app_name)

        if not blueprint:

            return


        frontend_path = blueprint["निर्देशिका"]["frontend"]

        index_file = os.path.join(frontend_path, "index.html")

        with open(index_file, "w", encoding="utf-8") as f:

            f.write(self.HTML_कोड(app_name))


        print("🕉️ फ्रंटएंड निर्मित:", index_file)


# test
if __name__ == "__main__":

    app_name = input("ऐप नाम लिखें: ")

    core = ब्रह्मफ्रंटएंडनिर्माताकोर()

    core.निर्माण(app_name)
