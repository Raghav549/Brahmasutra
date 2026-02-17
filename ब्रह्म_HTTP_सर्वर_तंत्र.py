# ब्रह्म HTTP सर्वर तंत्र

import http.server
import socketserver
import threading


class ब्रह्मHTTPसर्वर:

    def __init__(self, पोर्ट=8000):

        self.पोर्ट = पोर्ट
        self.सर्वर = None

        print("🕉️ ब्रह्म HTTP सर्वर तंत्र सक्रिय")


    def प्रारम्भ(self):

        handler = http.server.SimpleHTTPRequestHandler

        self.सर्वर = socketserver.TCPServer(
            ("", self.पोर्ट),
            handler
        )

        print(f"सर्वर प्रारम्भ: http://localhost:{self.पोर्ट}")

        thread = threading.Thread(
            target=self.सर्वर.serve_forever
        )

        thread.daemon = True
        thread.start()


    def रोकें(self):

        if self.सर्वर:
            self.सर्वर.shutdown()
            print("सर्वर रोका गया")


    def स्थिति(self):

        if self.सर्वर:
            print("सर्वर सक्रिय")
        else:
            print("सर्वर बंद")
