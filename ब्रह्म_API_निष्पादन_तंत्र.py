# ब्रह्म API निष्पादन तंत्र

import json
import importlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.parse

class ब्रह्मAPIHandler(BaseHTTPRequestHandler):

    routes = {}

    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/run":

            if "app" in query:

                app_name = query["app"][0]

                try:

                    module = importlib.import_module(app_name)

                    if hasattr(module, "main"):
                        module.main()

                        response = {
                            "status": "success",
                            "app": app_name,
                            "message": "application executed"
                        }

                    else:
                        response = {
                            "status": "error",
                            "message": "main function not found"
                        }

                except Exception as e:
                    response = {
                        "status": "error",
                        "message": str(e)
                    }

            else:
                response = {
                    "status": "error",
                    "message": "app parameter missing"
                }

        elif path in ब्रह्मAPIHandler.routes:

            response = ब्रह्मAPIHandler.routes[path]

        else:

            response = {
                "status": "error",
                "message": "route not found"
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())



class ब्रह्मAPIनिष्पादनतंत्र:

    def __init__(self, port=9100):

        self.port = port
        self.server = HTTPServer(("0.0.0.0", port), ब्रह्मAPIHandler)

        print("🕉️ ब्रह्म API निष्पादन तंत्र सक्रिय")
        print(f"API सर्वर प्रारम्भ: http://localhost:{port}")


    def मार्ग_जोड़ें(self, path, response):

        ब्रह्मAPIHandler.routes[path] = response


    def प्रारम्भ(self):

        threading.Thread(target=self.server.serve_forever).start()
