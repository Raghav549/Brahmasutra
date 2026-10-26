
import http.server
import socketserver
import json

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = {

                "status": "BRAHMA BACKEND RUNNING"

            }

            self.wfile.write(json.dumps(response).encode())

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        data = json.loads(post_data)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {

            "status": "SUCCESS",
            "received": data

        }

        self.wfile.write(json.dumps(response).encode())


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global httpd


    with socketserver.TCPServer(("", PORT), Handler) as httpd:

        print("🕉️ ब्रह्म बैकएंड सर्वर सक्रिय:", PORT)

        httpd.serve_forever()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
