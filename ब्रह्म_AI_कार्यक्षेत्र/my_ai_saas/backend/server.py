
# BRAHMA AUTO GENERATED BACKEND

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class BrahmaHandler(BaseHTTPRequestHandler):


    def do_GET(self):

        if self.path == "/":

            self.respond({
                "message": "BRAHMA BACKEND RUNNING"
            })


        elif self.path == "/health":

            self.respond({
                "status": "ok"
            })


        elif self.path == "/dashboard":

            self.respond({
                "dashboard": "active"
            })


    def do_POST(self):

        if self.path == "/login":

            self.respond({
                "status": "login_success"
            })


    def respond(self, data):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode()
        )


def run():

    server = HTTPServer(
        ("0.0.0.0", 7000),
        BrahmaHandler
    )

    print("BRAHMA BACKEND STARTED")

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
