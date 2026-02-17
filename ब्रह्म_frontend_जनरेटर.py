# 🕉️ BRAHMA FRONTEND GENERATOR

import os

class ब्रह्मfrontendजनरेटर:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        print("🕉️ ब्रह्म frontend जनरेटर सक्रिय")

    def निर्माण(self, app):

        frontend_path = os.path.join(self.base, app, "frontend")

        os.makedirs(frontend_path, exist_ok=True)

        index_file = os.path.join(frontend_path, "index.html")

        html = '''

<!DOCTYPE html>
<html>

<head>

<title>BRAHMA APP</title>

<style>

body {

background: black;
color: gold;
font-family: Arial;
text-align: center;
padding-top: 100px;

}

button {

background: gold;
color: black;
padding: 15px;
border: none;
font-size: 20px;
cursor: pointer;

}

</style>

</head>

<body>

<h1>🕉️ BRAHMA APPLICATION</h1>

<button onclick="checkBackend()">CHECK BACKEND</button>

<p id="result"></p>

<script>

function checkBackend(){

fetch("http://127.0.0.1:8000")

.then(res=>res.json())

.then(data=>{

document.getElementById("result").innerText = JSON.stringify(data)

})

.catch(err=>{

document.getElementById("result").innerText = "Backend not running"

})

}

</script>

</body>

</html>

'''

        with open(index_file, "w", encoding="utf-8") as f:
            f.write(html)

        print("🕉️ frontend निर्मित:", app)

        return index_file
