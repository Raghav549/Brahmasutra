

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT = 9000

users = {}

class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):

        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))

        if self.path == "/register":

            users[data["username"]] = data["password"]

            self._set_headers()
            self.wfile.write(json.dumps({"status":"registered"}).encode())

        elif self.path == "/login":

            if users.get(data["username"]) == data["password"]:

                self._set_headers()
                self.wfile.write(json.dumps({"status":"success"}).encode())

            else:

                self._set_headers()
                self.wfile.write(json.dumps({"status":"failed"}).encode())


def run():

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Backend running on {PORT}")
    server.serve_forever()


run()

