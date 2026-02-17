from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid

print("🕉️ BRAHMA BACKEND ACTIVE")

users = {}

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.end_headers()


    def do_POST(self):

        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length).decode()

        try:
            data = json.loads(body)
        except:
            data = {}

        if self.path == "/register":

            user = data.get("username")
            password = data.get("password")

            users[user] = password

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "status":"ok",
                "message":"registered"
            }).encode())


        elif self.path == "/login":

            user = data.get("username")
            password = data.get("password")

            if user in users and users[user] == password:

                token = str(uuid.uuid4())

                response = {
                    "status":"ok",
                    "token":token
                }

            else:

                response = {
                    "status":"error"
                }

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())


        else:

            self.send_response(404)
            self.end_headers()



server = HTTPServer(("0.0.0.0",7000),Handler)

print("SERVER RUNNING http://127.0.0.1:7000")

server.serve_forever()
