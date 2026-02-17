

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

