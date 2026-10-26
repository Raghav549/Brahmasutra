# ब्रह्म AI BACKEND निर्माता

import os


class ब्रह्मBackendनिर्माता:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_BACKEND")

        os.makedirs(self.base, exist_ok=True)


    def निर्मित(self, नाम):

        path = f"{self.base}/{नाम}"

        os.makedirs(path, exist_ok=True)


        server = f"{path}/server.py"


        code = '''

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

'''

        with open(server,"w",encoding="utf-8") as f:

            f.write(code)


        print("Backend निर्मित:", path)

        return path


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global maker

    print("🕉️ ब्रह्म AI Backend निर्माता सक्रिय")
    maker = ब्रह्मBackendनिर्माता()

    maker.निर्मित("chat_backend")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
