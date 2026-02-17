# ब्रह्म स्वतः बैकएंड जनक
# VERSION 123

import os

class ब्रह्मस्वतःबैकएंडजनक:

    def __init__(self, workspace):

        self.workspace = workspace

        self.backend_dir = os.path.join(workspace, "backend")

        if not os.path.exists(self.backend_dir):

            os.makedirs(self.backend_dir)

        print("ब्रह्म स्वतः बैकएंड जनक सक्रिय")


    def जनन(self, app_name):

        code = f'''

# BRAHMA Backend Server

from http.server import BaseHTTPRequestHandler, HTTPServer

class BrahmaHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.respond("Brahma Backend Running")

        elif self.path == "/health":

            self.respond("OK")

        elif self.path == "/dashboard":

            self.respond("Dashboard Ready")

        else:

            self.respond("Unknown endpoint")


    def do_POST(self):

        if self.path == "/login":

            self.respond("Login Success")

        else:

            self.respond("POST received")


    def respond(self, message):

        self.send_response(200)

        self.send_header("Content-type", "text/plain")

        self.end_headers()

        self.wfile.write(message.encode())


server = HTTPServer(("0.0.0.0", 5000), BrahmaHandler)

print("BRAHMA Backend LIVE at http://127.0.0.1:5000")

server.serve_forever()

'''

        path = os.path.join(self.backend_dir, "server.py")

        with open(path, "w", encoding="utf-8") as f:

            f.write(code)

        print("Backend generated:", path)

        return path
