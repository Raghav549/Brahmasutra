# 🕉️ ब्रह्म AI API निर्माता VERSION 21

import os

print("🕉️ ब्रह्म AI API निर्माता VERSION 21 सक्रिय")


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


# run

engine = ब्रह्मAPIनिर्माता()

name = input("API नाम लिखें: ")

engine.निर्मित(name)
