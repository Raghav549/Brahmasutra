
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
