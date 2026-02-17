import os

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

print("BRAHMA AUTO ENGINE V3 ACTIVE")

prompt = input("Enter App Prompt: ")

app = prompt.replace(" ","_")

path = BASE+"/"+app

backend = path+"/backend"
frontend = path+"/frontend"

os.makedirs(backend,exist_ok=True)
os.makedirs(frontend,exist_ok=True)

# BACKEND
backend_code = '''
from flask import Flask,request,jsonify
from flask_cors import CORS
import json,uuid,os

app = Flask(__name__)
CORS(app)

DB="users.json"

if not os.path.exists(DB):
 open(DB,"w").write("{}")

def load():
 return json.load(open(DB))

def save(d):
 json.dump(d,open(DB,"w"))

TOKENS={}

@app.route("/status")
def status():
 return jsonify({"status":"RUNNING"})

@app.route("/register",methods=["POST"])
def register():
 d=request.json
 u=d["username"]
 p=d["password"]

 db=load()

 if u in db:
  return jsonify({"status":"exists"})

 db[u]=p
 save(db)

 return jsonify({"status":"ok"})

@app.route("/login",methods=["POST"])
def login():
 d=request.json
 u=d["username"]
 p=d["password"]

 db=load()

 if u in db and db[u]==p:
  t=str(uuid.uuid4())
  TOKENS[t]=u
  return jsonify({"status":"ok","token":t})

 return jsonify({"status":"fail"})

@app.route("/dashboard")
def dash():

 t=request.headers.get("token")

 if t in TOKENS:
  return jsonify({"status":"ok","user":TOKENS[t]})

 return jsonify({"status":"unauthorized"})

app.run(host="0.0.0.0",port=9000)
'''

open(backend+"/server.py","w").write(backend_code)

# FRONTEND
frontend_code = '''
<html>

<body style="background:black;color:lime;text-align:center">

<h1>''' + app + '''</h1>

<input id="u" placeholder="username"><br><br>
<input id="p" placeholder="password" type="password"><br><br>

<button onclick="register()">REGISTER</button>
<button onclick="login()">LOGIN</button>
<button onclick="dashboard()">DASHBOARD</button>

<h3 id="result"></h3>

<script>

token=""

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
.then(d=>
{
token=d.token
result.innerText=JSON.stringify(d)
})
}

function dashboard()
{
fetch("http://127.0.0.1:9000/dashboard",
{
headers:{token:token}
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d))
}

</script>

</body>

</html>
'''

open(frontend+"/index.html","w").write(frontend_code)

print("FULL SaaS CREATED:",path)
