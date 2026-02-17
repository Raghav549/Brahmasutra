# 🕉️ BRAHMA AUTO EXECUTION API ENGINE

import os
from flask import Flask, request, jsonify

class ब्रह्मस्वचालितनिष्पादन:

    def __init__(self):
        print("🕉️ ब्रह्म स्वचालित निष्पादन इंजन सक्रिय")

        self.app = Flask(__name__)

        self.स्थापित_पथ = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_स्थापित"
        )

        os.makedirs(self.स्थापित_पथ, exist_ok=True)

        self.routes()

    def routes(self):

        @self.app.route("/run", methods=["POST"])
        def run_app():

            data = request.json

            नाम = data.get("app")

            if not नाम:
                return jsonify({"status":"error","message":"app name required"})

            path = os.path.join(self.स्थापित_पथ, नाम)

            if not os.path.exists(path):
                return jsonify({"status":"error","message":"app not found"})

            try:

                code = ""

                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()

                print("🕉️ अनुप्रयोग निष्पादन:", नाम)

                exec(code, globals())

                return jsonify({
                    "status":"success",
                    "message":"app executed",
                    "app":नाम
                })

            except Exception as e:

                return jsonify({
                    "status":"error",
                    "message":str(e)
                })


    def प्रारम्भ(self):

        print("🕉️ ब्रह्म API सर्वर प्रारम्भ")

        self.app.run(
            host="0.0.0.0",
            port=7005,
            debug=False
        )


if __name__ == "__main__":

    engine = ब्रह्मस्वचालितनिष्पादन()

    engine.प्रारम्भ()
