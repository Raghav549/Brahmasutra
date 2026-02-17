
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
