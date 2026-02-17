from http.server import HTTPServer, BaseHTTPRequestHandler
import json

HOST = "127.0.0.1"
PORT = 8080


class ब्रह्मHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        response = {
            "ब्रह्म": "सक्रिय",
            "engine": "ब्रह्म_HTTP_इंजन",
            "version": "94",
            "status": "running"
        }

        self.send_response(200)

        self.send_header("Content-Type", "application/json; charset=utf-8")

        self.end_headers()

        self.wfile.write(
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )


def प्रारंभ():

    server = HTTPServer((HOST, PORT), ब्रह्मHTTPHandler)

    print(f"ब्रह्म HTTP इंजन प्रारंभ: http://{HOST}:{PORT}")

    server.serve_forever()


if __name__ == "__main__":

    प्रारंभ()
