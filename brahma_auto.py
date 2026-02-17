import os

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

print("BRAHMA AUTO GENERATOR ACTIVE")

prompt = input("Enter App Prompt: ")

app_name = prompt.replace(" ","_")

app_path = BASE + "/" + app_name

backend = app_path + "/backend"
frontend = app_path + "/frontend"

os.makedirs(backend, exist_ok=True)
os.makedirs(frontend, exist_ok=True)

# backend create
backend_code = '''
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/status")
def status():
    return jsonify({"status":"RUNNING","app":"''' + app_name + '''"})

app.run(host="0.0.0.0",port=9000)
'''

open(backend+"/server.py","w").write(backend_code)

# frontend create
frontend_code = '''
<html>
<body style="background:black;color:lime;text-align:center">

<h1>''' + app_name + '''</h1>

<button onclick="check()">CHECK BACKEND</button>

<h3 id="result"></h3>

<script>

function check()
{
fetch("http://127.0.0.1:9000/status")
.then(r=>r.json())
.then(d=>{
document.getElementById("result").innerText=
JSON.stringify(d)
})
}

</script>

</body>
</html>
'''

open(frontend+"/index.html","w").write(frontend_code)

print("APP CREATED:", app_path)
