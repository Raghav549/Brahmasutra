from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8080


def मुख्य():
    return "🕉️ BRAHMA SERVER SUCCESSFULLY RUNNING"


class ब्रह्मHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        response = मुख्य()

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        self.wfile.write(response.encode("utf-8"))


def प्रारंभ():

    server = HTTPServer((HOST, PORT), ब्रह्मHandler)

    print(f"ब्रह्म सर्वर प्रारंभ: http://{HOST}:{PORT}")

    server.serve_forever()


if __name__ == "__main__":
    प्रारंभ()
