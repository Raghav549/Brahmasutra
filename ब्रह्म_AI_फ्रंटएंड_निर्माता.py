# 🕉️ ब्रह्म AI फ्रंटएंड निर्माता VERSION 44 FIXED

import os


class ब्रह्मफ्रंटएंडनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म फ्रंटएंड निर्माता सक्रिय")


    def निर्माण(self, app_name):

        base = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग/" + app_name
        )

        frontend_path = base + "/frontend"

        os.makedirs(frontend_path, exist_ok=True)

        html_file = frontend_path + "/index.html"

        html = '''
<!DOCTYPE html>
<html>

<head>

<title>BRAHMA APP</title>

<style>

body {

background: black;
color: lime;
font-family: monospace;
text-align: center;
margin-top: 100px;

}

button {

padding: 10px;
font-size: 20px;

}

</style>

</head>

<body>

<h1>🕉️ BRAHMA APP RUNNING</h1>

<button onclick="run()">CHECK BACKEND</button>

<p id="status"></p>

<script>

function run() {

fetch("http://127.0.0.1:7000/")

.then(r => r.json())

.then(d => {

document.getElementById("status").innerHTML =
"Backend: " + d.status

})

.catch(e => {

document.getElementById("status").innerHTML =
"Backend not reachable"

})

}

</script>

</body>

</html>
'''

        with open(html_file, "w", encoding="utf-8") as f:

            f.write(html)


        print("Frontend निर्मित:", frontend_path)
