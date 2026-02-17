
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


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("🕉️ ब्रह्म बैकएंड सर्वर सक्रिय:", PORT)

    httpd.serve_forever()
