from http.server import HTTPServer, BaseHTTPRequestHandler
import json

HOST = "127.0.0.1"
PORT = 8080


class ब्रह्मHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        response = {
            "ब्रह्म": "सक्रिय",
            "engine": "ब्रह्म_HTTP_इंजन",
            "version": "94",
            "status": "running"
        }

        self.send_response(200)

        self.send_header("Content-Type", "application/json; charset=utf-8")

        self.end_headers()

        self.wfile.write(
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )


def प्रारंभ():

    server = HTTPServer((HOST, PORT), ब्रह्मHTTPHandler)

    print(f"ब्रह्म HTTP इंजन प्रारंभ: http://{HOST}:{PORT}")

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
