
# BRAHMA AUTO GENERATED BACKEND

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class BrahmaHandler(BaseHTTPRequestHandler):


    def do_GET(self):

        if self.path == "/":

            self.respond({
                "message": "BRAHMA BACKEND RUNNING"
            })


        elif self.path == "/health":

            self.respond({
                "status": "ok"
            })


        elif self.path == "/dashboard":

            self.respond({
                "dashboard": "active"
            })


    def do_POST(self):

        if self.path == "/login":

            self.respond({
                "status": "login_success"
            })


    def respond(self, data):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode()
        )


def run():

    server = HTTPServer(
        ("0.0.0.0", 7000),
        BrahmaHandler
    )

    print("BRAHMA BACKEND STARTED")

    server.serve_forever()


if __name__ == "__main__":

    run()
