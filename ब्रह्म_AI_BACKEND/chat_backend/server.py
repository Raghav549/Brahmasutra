

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


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    run()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
