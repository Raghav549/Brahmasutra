# BRAHMA AUTO BACKEND LOGIC ENGINE

import os

print("🕉️ ब्रह्म बैकेंड तर्क निर्माता सक्रिय")

BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_APPS")

os.makedirs(BASE, exist_ok=True)



class ब्रह्मबैकेंडनिर्माता:


    def निर्मित(self,name):

        path = f"{BASE}/{name}/backend"

        os.makedirs(path, exist_ok=True)


        code = '''
from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    users[data["username"]] = data["password"]

    return jsonify({"status":"registered"})


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    if users.get(data["username"]) == data["password"]:

        return jsonify({"status":"success"})

    return jsonify({"status":"failed"})


@app.route("/")
def home():

    return "BRAHMA BACKEND ACTIVE"


if __name__ == "__main__":

    app.run(port=5000)
'''

        open(path+"/server.py","w").write(code)

        print("Backend logic निर्मित:",path)



if __name__ == "__main__":

    name = input("App name: ")

    b = ब्रह्मबैकेंडनिर्माता()

    b.निर्मित(name)
