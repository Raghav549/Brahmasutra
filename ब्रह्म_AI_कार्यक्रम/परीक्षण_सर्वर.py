from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8080


def मुख्य():
    return "🕉️ BRAHMA SERVER SUCCESSFULLY RUNNING"


class ब्रह्मHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        response = मुख्य()

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        self.wfile.write(response.encode("utf-8"))


def प्रारंभ():

    server = HTTPServer((HOST, PORT), ब्रह्मHandler)

    print(f"ब्रह्म सर्वर प्रारंभ: http://{HOST}:{PORT}")

    server.serve_forever()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    प्रारंभ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
