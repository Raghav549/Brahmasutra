
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status":"running"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    return jsonify({"status":"registered","user":data.get("username")})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    return jsonify({"status":"logged_in","user":data.get("username")})

@app.route("/dashboard")
def dashboard():
    return jsonify({"dashboard":"active"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
