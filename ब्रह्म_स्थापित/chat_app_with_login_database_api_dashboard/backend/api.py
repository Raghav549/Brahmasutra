
# 🕉️ ब्रह्म API बैकएंड

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def मुख्य():

    return jsonify({

        "status": "running",

        "engine": "BRAHMA"

    })


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=7000)
