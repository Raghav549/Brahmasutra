# 🕉️ ब्रह्म AI Frontend निर्माता VERSION 19

import os

print("🕉️ ब्रह्म AI Frontend निर्माता VERSION 19 सक्रिय")


class ब्रह्मFrontendनिर्माता:

    def __init__(self):

        self.base_path = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_frontend")

        os.makedirs(self.base_path, exist_ok=True)

    def निर्मित(self, name):

        app_path = os.path.join(self.base_path, name)

        os.makedirs(app_path, exist_ok=True)

        html = """
<!DOCTYPE html>
<html>
<head>
<title>BRAHMA APP</title>
</head>

<body>

<h1>BRAHMA AI GENERATED APP</h1>

<h2>Login</h2>

<input id="user" placeholder="username">
<input id="pass" placeholder="password" type="password">

<button onclick="login()">Login</button>

<h2>Dashboard</h2>

<div id="output"></div>

<script>

function login(){

document.getElementById("output").innerHTML =
"Login success (simulated)"

}

</script>

</body>

</html>
"""

        file = os.path.join(app_path, "index.html")

        with open(file,"w") as f:

            f.write(html)

        print("Frontend निर्मित:", app_path)

        return app_path


# test

builder = ब्रह्मFrontendनिर्माता()

name = input("App नाम लिखें: ")

builder.निर्मित(name)
