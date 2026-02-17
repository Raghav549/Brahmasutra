from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT = 8123


class BrahmaHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = {
                "status": "success",
                "system": "BRAHMA",
                "message": "backend connected successfully"
            }

            self.wfile.write(json.dumps(response).encode())

        else:

            self.send_response(404)
            self.end_headers()


server = HTTPServer(("0.0.0.0", PORT), BrahmaHandler)

print("🕉️ BRAHMA BACKEND RUNNING:", PORT)

server.serve_forever()
