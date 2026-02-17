import os

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

print("BRAHMA AUTO ENGINE V2 ACTIVE")

prompt = input("Enter App Prompt: ")

app_name = prompt.replace(" ","_")

app_path = BASE + "/" + app_name

backend = app_path + "/backend"
frontend = app_path + "/frontend"

os.makedirs(backend, exist_ok=True)
os.makedirs(frontend, exist_ok=True)

# backend
backend_code = '''
from flask import Flask,request,jsonify
from flask_cors import CORS
import json,os,uuid

app = Flask(__name__)
CORS(app)

DB="users.json"

if not os.path.exists(DB):
    open(DB,"w").write("{}")

def load():
    return json.load(open(DB))

def save(d):
    json.dump(d,open(DB,"w"))

@app.route("/status")
def status():
    return jsonify({"status":"RUNNING"})

@app.route("/register",methods=["POST"])
def register():
    data=request.json
    u=data["username"]
    p=data["password"]
    db=load()
    if u in db:
        return jsonify({"status":"exists"})
    db[u]=p
    save(db)
    return jsonify({"status":"ok"})

@app.route("/login",methods=["POST"])
def login():
    data=request.json
    u=data["username"]
    p=data["password"]
    db=load()
    if u in db and db[u]==p:
        return jsonify({"status":"ok","token":str(uuid.uuid4())})
    return jsonify({"status":"fail"})

app.run(host="0.0.0.0",port=9000)
'''

open(backend+"/server.py","w").write(backend_code)

# frontend
frontend_code = '''
<html>
<body style="background:black;color:lime;text-align:center">

<h1>''' + app_name + '''</h1>

<input id="u" placeholder="username"><br><br>
<input id="p" placeholder="password" type="password"><br><br>

<button onclick="register()">REGISTER</button>
<button onclick="login()">LOGIN</button>
<button onclick="check()">STATUS</button>

<h3 id="result"></h3>

<script>

function register()
{
fetch("http://127.0.0.1:9000/register",
{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:u.value,
password:p.value
})
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d))
}

function login()
{
fetch("http://127.0.0.1:9000/login",
{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:u.value,
password:p.value
})
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d))
}

function check()
{
fetch("http://127.0.0.1:9000/status")
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d))
}

</script>

</body>
</html>
'''

open(frontend+"/index.html","w").write(frontend_code)

print("FULL APP CREATED:", app_path)
