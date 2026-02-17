from http.server import HTTPServer,BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path=="/test":

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()

            self.wfile.write(b"BRAHMA AI SUCCESS")

server=HTTPServer(("0.0.0.0",7000),H)

print("BACKEND RUNNING")

server.serve_forever()
