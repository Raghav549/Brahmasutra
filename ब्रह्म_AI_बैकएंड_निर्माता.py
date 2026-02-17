import os

class ब्रह्मबैकएंडनिर्माता:

    def __init__(self):
        print("🕉️ ब्रह्म बैकएंड निर्माता सक्रिय")

    def निर्माण(self, app_name):

        base = os.path.expanduser(
            f"~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग/{app_name}/backend"
        )

        os.makedirs(base, exist_ok=True)

        server_code = '''
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
'''

        with open(base + "/server.py", "w", encoding="utf-8") as f:
            f.write(server_code)

        print("Backend निर्मित:", base)
