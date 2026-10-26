from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid

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


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global server

    print("🕉️ BRAHMA BACKEND ACTIVE")



    server = HTTPServer(("0.0.0.0",7000),Handler)

    print("SERVER RUNNING http://127.0.0.1:7000")

    server.serve_forever()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
