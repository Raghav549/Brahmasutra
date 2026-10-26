

import http.server
import socketserver

PORT = 9090

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type","text/plain")

        self.end_headers()

        self.wfile.write(b"BRAHMA API RUNNING")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global httpd


    with socketserver.TCPServer(("", PORT), Handler) as httpd:

        print("BRAHMA API STARTED:", PORT)

        httpd.serve_forever()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
