from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(b"BRAHMA Backend LIVE")

server = HTTPServer(("0.0.0.0", 5000), Handler)

print("BRAHMA Backend LIVE at http://127.0.0.1:5000")

server.serve_forever()
