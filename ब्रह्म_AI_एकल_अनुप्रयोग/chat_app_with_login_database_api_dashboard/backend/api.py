
# 🕉️ BRAHMA AI BACKEND

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api")
def api():

    return jsonify({
        "status":"ok",
        "app":"chat app with login database api dashboard",
        "engine":"BRAHMA AI VERSION 36"
    })

if __name__ == "__main__":
    app.run(port=5000)
