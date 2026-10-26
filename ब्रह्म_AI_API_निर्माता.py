# 🕉️ ब्रह्म AI API निर्माता VERSION 21

import os


class ब्रह्मAPIनिर्माता:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_API")

        os.makedirs(self.base, exist_ok=True)


    def निर्मित(self, name):

        path = os.path.join(self.base, name)

        os.makedirs(path, exist_ok=True)

        server = '''

import http.server
import socketserver

PORT = 9090

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type","text/plain")

        self.end_headers()

        self.wfile.write(b"BRAHMA API RUNNING")


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("BRAHMA API STARTED:", PORT)

    httpd.serve_forever()

'''

        file = os.path.join(path,"server.py")

        with open(file,"w") as f:

            f.write(server)


        print("API निर्मित:", file)

        return file


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global engine, name

    print("🕉️ ब्रह्म AI API निर्माता VERSION 21 सक्रिय")


    # run

    engine = ब्रह्मAPIनिर्माता()

    name = input("API नाम लिखें: ")

    engine.निर्मित(name)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
