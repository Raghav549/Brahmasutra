# 🕉️ BRAHMA BACKEND GENERATOR ENGINE
# VERSION 111
# FULL SANSKRIT BACKEND GENERATOR

import os
import json

print("🕉️ ब्रह्म बैकएंड निर्माता कोर सक्रिय (VERSION 111)")


class ब्रह्मबैकएंडनिर्माताकोर:

    def __init__(self):

        self.base_path = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/ब्रह्म_अनुप्रयोग"
        )


    # blueprint load
    def रूपरेखा_लोड(self, app_name):

        blueprint_path = os.path.join(
            self.base_path,
            app_name,
            "config",
            "brahma_blueprint.json"
        )

        if not os.path.exists(blueprint_path):

            print("त्रुटि: blueprint नहीं मिला")
            return None

        with open(blueprint_path, "r", encoding="utf-8") as f:

            return json.load(f)


    # backend server code generate
    def सर्वर_कोड(self):

        code = '''
import http.server
import socketserver
import json

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = {

                "status": "BRAHMA BACKEND RUNNING"

            }

            self.wfile.write(json.dumps(response).encode())

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        data = json.loads(post_data)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {

            "status": "SUCCESS",
            "received": data

        }

        self.wfile.write(json.dumps(response).encode())


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("🕉️ ब्रह्म बैकएंड सर्वर सक्रिय:", PORT)

    httpd.serve_forever()
'''

        return code


    # backend generate
    def निर्माण(self, app_name):

        blueprint = self.रूपरेखा_लोड(app_name)

        if not blueprint:

            return


        backend_path = blueprint["निर्देशिका"]["backend"]

        server_file = os.path.join(backend_path, "server.py")

        with open(server_file, "w", encoding="utf-8") as f:

            f.write(self.सर्वर_कोड())


        print("🕉️ बैकएंड निर्मित:", server_file)


# test
if __name__ == "__main__":

    app_name = input("ऐप नाम लिखें: ")

    core = ब्रह्मबैकएंडनिर्माताकोर()

    core.निर्माण(app_name)
