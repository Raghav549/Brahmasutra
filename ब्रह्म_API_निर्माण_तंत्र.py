# ब्रह्म API निर्माण तंत्र

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class ब्रह्मAPIHandler(BaseHTTPRequestHandler):

    routes = {}


    def do_GET(self):

        path = self.path

        if path in ब्रह्मAPIHandler.routes:

            response = ब्रह्मAPIHandler.routes[path]()

            self.send_response(200)
            self.send_header(
                "Content-type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length)

        data = json.loads(body)

        path = self.path

        if path in ब्रह्मAPIHandler.routes:

            response = ब्रह्मAPIHandler.routes[path](data)

            self.send_response(200)
            self.send_header(
                "Content-type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        else:

            self.send_response(404)
            self.end_headers()



class ब्रह्मAPIनिर्माता:


    def __init__(self, पोर्ट=9000):

        self.पोर्ट = पोर्ट
        self.server = None

        print("🕉️ ब्रह्म API निर्माण तंत्र सक्रिय")


    def मार्ग_जोड़ें(self, path, function):

        ब्रह्मAPIHandler.routes[path] = function

        print(f"API मार्ग जोड़ा: {path}")


    def प्रारम्भ(self):

        self.server = HTTPServer(
            ("", self.पोर्ट),
            ब्रह्मAPIHandler
        )

        print(f"API सर्वर प्रारम्भ: http://localhost:{self.पोर्ट}")

        thread = threading.Thread(
            target=self.server.serve_forever
        )

        thread.daemon = True
        thread.start()


    def रोकें(self):

        if self.server:
            self.server.shutdown()
            print("API सर्वर रोका गया")
