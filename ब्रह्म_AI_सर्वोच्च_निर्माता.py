# ब्रह्म_AI_सर्वोच्च_निर्माता.py
# VERSION 44 FINAL ASCENSION

import os

from brahma_templates import write_chat_server
import subprocess
import sys
import threading
import http.server
import socketserver


class ब्रह्मसर्वोच्चनिर्माता:

    def __init__(self):
        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

    def विश्लेषण(self, prompt):

        name = prompt.lower().replace(" ", "_")

        return name

    def backend_निर्माण(self, app):

        path = f"{self.base}/{app}/backend"

        os.makedirs(path, exist_ok=True)

        written = write_chat_server(path, app)

        return written

    def frontend_निर्माण(self, app):

        path = f"{self.base}/{app}/frontend"

        os.makedirs(path, exist_ok=True)

        code = '''
<html>
<body style="background:black;color:lime;text-align:center">

<h1>BRAHMA AI APP LIVE</h1>

<button onclick="check()">CHECK BACKEND</button>

<p id="result"></p>

<script>

function check(){

fetch("http://127.0.0.1:9000/status")
.then(r=>r.json())
.then(d=>{

document.getElementById("result").innerText=d.status

})

}

</script>

</body>
</html>
'''

        open(path + "/index.html", "w").write(code)

        return path

    def backend_run(self, path):

        def run():
            subprocess.run([sys.executable, path + "/server.py"])

        threading.Thread(target=run).start()

    def frontend_run(self, path):

        os.chdir(path)

        handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", 8080), handler) as httpd:

            print("🌐 FRONTEND LIVE: http://127.0.0.1:8080")

            httpd.serve_forever()

    def निर्माण(self, prompt):

        app = self.विश्लेषण(prompt)

        print("APP:", app)

        backend = self.backend_निर्माण(app)

        frontend = self.frontend_निर्माण(app)

        print("BACKEND CREATED")

        print("FRONTEND CREATED")

        print("STARTING BACKEND...")

        self.backend_run(backend)

        print("STARTING FRONTEND...")

        self.frontend_run(frontend)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global brahma, prompt

    print("🕉️ BRAHMA AI VERSION 44 FINAL ASCENSION ACTIVE")
    brahma = ब्रह्मसर्वोच्चनिर्माता()

    prompt = input("PROMPT: ")

    brahma.निर्माण(prompt)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
