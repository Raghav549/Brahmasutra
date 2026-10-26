

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


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global server


    server = HTTPServer(("0.0.0.0", 5000), BrahmaHandler)

    print("BRAHMA Backend LIVE at http://127.0.0.1:5000")

    server.serve_forever()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
