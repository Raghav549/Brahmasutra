import os

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

print("BRAHMA AUTO ENGINE V4 ACTIVE")

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

USER_DB="users.json"
CHAT_DB="chat.json"

if not os.path.exists(USER_DB):
 open(USER_DB,"w").write("{}")

if not os.path.exists(CHAT_DB):
 open(CHAT_DB,"w").write("[]")

def load_users():
 return json.load(open(USER_DB))

def save_users(d):
 json.dump(d,open(USER_DB,"w"))

def load_chat():
 return json.load(open(CHAT_DB))

def save_chat(d):
 json.dump(d,open(CHAT_DB,"w"))

TOKENS={}

@app.route("/status")
def status():
 return jsonify({"status":"RUNNING"})

@app.route("/register",methods=["POST"])
def register():

 d=request.json
 u=d["username"]
 p=d["password"]

 db=load_users()

 if u in db:
  return jsonify({"status":"exists"})

 db[u]=p
 save_users(db)

 return jsonify({"status":"ok"})

@app.route("/login",methods=["POST"])
def login():

 d=request.json
 u=d["username"]
 p=d["password"]

 db=load_users()

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

@app.route("/send",methods=["POST"])
def send():

 t=request.headers.get("token")

 if t not in TOKENS:
  return jsonify({"status":"unauthorized"})

 d=request.json

 chat=load_chat()

 chat.append({
  "user":TOKENS[t],
  "msg":d["msg"]
 })

 save_chat(chat)

 return jsonify({"status":"sent"})

@app.route("/chat")
def chat():

 return jsonify(load_chat())

app.run(host="0.0.0.0",port=9100)
'''

open(backend+"/server.py","w").write(backend_code)

# FRONTEND
frontend_code = '''
<html>

<body style="background:black;color:lime;text-align:center">

<h1>''' + app + '''</h1>

<input id="u" placeholder="username"><br>
<input id="p" placeholder="password" type="password"><br>

<button onclick="register()">REGISTER</button>
<button onclick="login()">LOGIN</button>
<button onclick="dashboard()">DASHBOARD</button>

<hr>

<input id="msg" placeholder="message">

<button onclick="send()">SEND</button>
<button onclick="load()">LOAD CHAT</button>

<pre id="result"></pre>

<script>

token=""

function register()
{
fetch("http://127.0.0.1:9100/register",
{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:u.value,
password:p.value
})
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

function login()
{
fetch("http://127.0.0.1:9100/login",
{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:u.value,
password:p.value
})
})
.then(r=>r.json())
.then(d=>{
token=d.token
result.innerText=JSON.stringify(d,null,2)
})
}

function dashboard()
{
fetch("http://127.0.0.1:9100/dashboard",
{
headers:{token:token}
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

function send()
{
fetch("http://127.0.0.1:9100/send",
{
method:"POST",
headers:{
"Content-Type":"application/json",
token:token
},
body:JSON.stringify({
msg:msg.value
})
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

function load()
{
fetch("http://127.0.0.1:9100/chat")
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

</script>

</body>

</html>
'''

open(frontend+"/index.html","w").write(frontend_code)

print("REAL CHAT SaaS CREATED:",path)
