# 🕉️ BRAHMA BACKEND SERVER GENERATOR

import os

class ब्रह्मbackendजनरेटर:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        print("🕉️ ब्रह्म backend जनरेटर सक्रिय")

    def निर्माण(self, app):

        backend_path = os.path.join(self.base, app, "backend")

        os.makedirs(backend_path, exist_ok=True)

        server_file = os.path.join(backend_path, "server.py")

        code = '''

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = {
                "status": "running",
                "system": "brahma backend"
            }

            self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("localhost", 8000), Handler)

print("🕉️ BRAHMA backend running on port 8000")

server.serve_forever()

'''

        with open(server_file, "w", encoding="utf-8") as f:
            f.write(code)

        print("🕉️ backend निर्मित:", app)

        return server_file
