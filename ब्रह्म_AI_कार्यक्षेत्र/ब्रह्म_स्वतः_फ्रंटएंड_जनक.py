# ब्रह्म स्वतः फ्रंटएंड जनक
# VERSION 122

import os

class ब्रह्मस्वतःफ्रंटएंडजनक:

    def __init__(self, workspace):

        self.workspace = workspace

        self.frontend_dir = os.path.join(workspace, "frontend")

        if not os.path.exists(self.frontend_dir):

            os.makedirs(self.frontend_dir)

        print("ब्रह्म स्वतः फ्रंटएंड जनक सक्रिय")


    def जनन(self, app_name):

        html = f"""
<!DOCTYPE html>
<html>
<head>

<title>{app_name}</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body {{

background: #0b1220;
color: white;
font-family: Arial;
text-align: center;
margin-top: 100px;

}}

input {{

padding: 10px;
margin: 10px;
width: 250px;

}}

button {{

padding: 12px;
background: #00ff88;
border: none;
cursor: pointer;

}}

.container {{

background: #111a33;
padding: 30px;
display: inline-block;

}}

</style>

</head>

<body>

<div class="container">

<h1>BRAHMA APP: {app_name}</h1>

<h2>Login</h2>

<input placeholder="Username"><br>
<input placeholder="Password" type="password"><br>

<button onclick="login()">Login</button>

<h2>Dashboard</h2>

<button onclick="testBackend()">Test Backend</button>

</div>

<script>

function login() {{

alert("Login system ready");

}}

function testBackend() {{

fetch("http://127.0.0.1:5000")

.then(res=>res.text())

.then(data=>alert(data))

}}

</script>

</body>
</html>
"""

        path = os.path.join(self.frontend_dir, "index.html")

        with open(path, "w", encoding="utf-8") as f:

            f.write(html)

        print("Frontend generated:", path)

        return path
