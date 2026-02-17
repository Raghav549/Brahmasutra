import os

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

print("BRAHMA AUTO ENGINE V5 ACTIVE")

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
ADMIN_DB="admin.json"

if not os.path.exists(USER_DB):
 open(USER_DB,"w").write("{}")

if not os.path.exists(CHAT_DB):
 open(CHAT_DB,"w").write("[]")

if not os.path.exists(ADMIN_DB):
 open(ADMIN_DB,"w").write('{"admin":"admin123"}')

def load_users():
 return json.load(open(USER_DB))

def save_users(d):
 json.dump(d,open(USER_DB,"w"))

def load_chat():
 return json.load(open(CHAT_DB))

def save_chat(d):
 json.dump(d,open(CHAT_DB,"w"))

def load_admin():
 return json.load(open(ADMIN_DB))

TOKENS={}
ADMIN_TOKENS={}

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

@app.route("/admin_login",methods=["POST"])
def admin_login():

 d=request.json
 u=d["username"]
 p=d["password"]

 db=load_admin()

 if u in db and db[u]==p:
  t=str(uuid.uuid4())
  ADMIN_TOKENS[t]=u
  return jsonify({"status":"ok","token":t})

 return jsonify({"status":"fail"})

@app.route("/users")
def users():

 t=request.headers.get("token")

 if t not in ADMIN_TOKENS:
  return jsonify({"status":"unauthorized"})

 return jsonify(load_users())

@app.route("/delete_user",methods=["POST"])
def delete_user():

 t=request.headers.get("token")

 if t not in ADMIN_TOKENS:
  return jsonify({"status":"unauthorized"})

 d=request.json
 u=d["username"]

 db=load_users()

 if u in db:
  del db[u]
  save_users(db)

 return jsonify({"status":"deleted"})

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

app.run(host="0.0.0.0",port=9200)
'''

open(backend+"/server.py","w").write(backend_code)

# FRONTEND
frontend_code = '''
<html>

<body style="background:black;color:lime;text-align:center">

<h1>''' + app + ''' ADMIN SaaS</h1>

<input id="u" placeholder="username"><br>
<input id="p" placeholder="password"><br>

<button onclick="register()">REGISTER</button>
<button onclick="login()">LOGIN</button>

<hr>

<h3>ADMIN</h3>

<input id="au" placeholder="admin username"><br>
<input id="ap" placeholder="admin password"><br>

<button onclick="admin_login()">ADMIN LOGIN</button>
<button onclick="load_users()">LOAD USERS</button>

<hr>

<input id="msg" placeholder="message">

<button onclick="send()">SEND</button>
<button onclick="load_chat()">LOAD CHAT</button>

<pre id="result"></pre>

<script>

token=""
admin_token=""

function register()
{
fetch("http://127.0.0.1:9200/register",
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
fetch("http://127.0.0.1:9200/login",
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

function admin_login()
{
fetch("http://127.0.0.1:9200/admin_login",
{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:au.value,
password:ap.value
})
})
.then(r=>r.json())
.then(d=>{
admin_token=d.token
result.innerText=JSON.stringify(d,null,2)
})
}

function load_users()
{
fetch("http://127.0.0.1:9200/users",
{
headers:{token:admin_token}
})
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

function send()
{
fetch("http://127.0.0.1:9200/send",
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

function load_chat()
{
fetch("http://127.0.0.1:9200/chat")
.then(r=>r.json())
.then(d=>result.innerText=JSON.stringify(d,null,2))
}

</script>

</body>

</html>
'''

open(frontend+"/index.html","w").write(frontend_code)

print("ADMIN SaaS CREATED:",path)
