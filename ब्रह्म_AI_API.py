# ब्रह्म AI API ENGINE

import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

print("🕉️ ब्रह्म AI API Engine सक्रिय")


BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_API")

os.makedirs(BASE, exist_ok=True)

DB = f"{BASE}/data.db"


if not os.path.exists(DB):

    with open(DB,"w",encoding="utf-8") as f:

        json.dump({},f)



class Handler(BaseHTTPRequestHandler):


    def _response(self,data):

        self.send_response(200)

        self.send_header("Content-Type","application/json")

        self.end_headers()

        self.wfile.write(json.dumps(data).encode())


    def do_GET(self):

        with open(DB,"r",encoding="utf-8") as f:

            data = json.load(f)

        self._response(data)


    def do_POST(self):

        length = int(self.headers['Content-Length'])

        body = self.rfile.read(length)

        obj = json.loads(body)

        with open(DB,"r",encoding="utf-8") as f:

            data = json.load(f)

        data.update(obj)

        with open(DB,"w",encoding="utf-8") as f:

            json.dump(data,f)

        self._response({"status":"saved"})



def start():

    server = HTTPServer(("0.0.0.0",9000),Handler)

    print("API running on port 9000")

    server.serve_forever()



if __name__ == "__main__":

    start()
