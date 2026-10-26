# ब्रह्म API निष्पादन तंत्र
#
# एक छोटा HTTP API रनर। मार्ग (routes) पंजीकृत किए जा सकते हैं और अनुरोध
# आने पर चलाए जाते हैं। यह मॉड्यूल अब GET और POST दोनों का समर्थन करता है,
# त्रुटियों को JSON के रूप में लौटाता है और सर्वर को थ्रेड में चलाता है।

import importlib
import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class ब्रह्मAPIHandler(BaseHTTPRequestHandler):
    """हर अनुरोध को JSON उत्तर देने वाला handler।"""

    routes = {}
    post_routes = {}

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        # डिफ़ॉल्ट access log शोर कम करें; चाहें तो इसे override करें।
        return

    # -- helpers ---------------------------------------------------------
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _resolve(handler, *args):
        return handler(*args) if callable(handler) else handler

    # -- HTTP verbs ------------------------------------------------------
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ("/", "/health"):
            self._send(200, {"status": "running", "engine": "BRAHMA"})
            return

        if path == "/run":
            app_name = query.get("app", [None])[0]
            if not app_name:
                self._send(400, {"status": "error", "message": "app parameter missing"})
                return
            try:
                module = importlib.import_module(app_name)
            except Exception as exc:  # noqa: BLE001 - report to caller
                self._send(404, {"status": "error", "message": str(exc)})
                return
            if not hasattr(module, "main"):
                self._send(404, {"status": "error", "message": "main function not found"})
                return
            try:
                result = module.main()
            except Exception as exc:  # noqa: BLE001
                self._send(500, {"status": "error", "message": str(exc)})
                return
            self._send(200, {"status": "success", "app": app_name, "result": result})
            return

        if path in self.routes:
            try:
                response = self._resolve(self.routes[path])
            except Exception as exc:  # noqa: BLE001
                self._send(500, {"status": "error", "message": str(exc)})
                return
            self._send(200, response)
            return

        self._send(404, {"status": "error", "message": "route not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""

        try:
            data = json.loads(body.decode("utf-8")) if body else {}
        except (ValueError, UnicodeDecodeError):
            self._send(400, {"status": "error", "message": "invalid JSON body"})
            return

        handler = self.post_routes.get(path) or self.routes.get(path)
        if handler is None:
            self._send(404, {"status": "error", "message": "route not found"})
            return

        try:
            response = self._resolve(handler, data)
        except Exception as exc:  # noqa: BLE001
            self._send(500, {"status": "error", "message": str(exc)})
            return
        self._send(200, response)


class _पुनःप्रयोगयोग्यसर्वर(HTTPServer):
    """``HTTPServer`` with ``SO_REUSEADDR``.

    Without it, an immediately following run of the same demo fails with
    ``OSError: [Errno 98] Address already in use`` while the previous socket is
    still in ``TIME_WAIT`` — which is exactly what happened in the test suite.
    """

    allow_reuse_address = True
    daemon_threads = True


class ब्रह्मAPIनिष्पादनतंत्र:
    """API सर्वर का प्रबंधक।"""

    def __init__(self, port=9100):
        self.port = port
        self.server = _पुनःप्रयोगयोग्यसर्वर(("0.0.0.0", port), ब्रह्मAPIHandler)
        self.thread = None
        print("🕉️ ब्रह्म API निष्पादन तंत्र सक्रिय")
        print(f"API सर्वर प्रारम्भ: http://localhost:{port}")

    def मार्ग_जोड़ें(self, path, response):
        """GET मार्ग जोड़ें (कॉलबल या स्थिर JSON)।"""
        ब्रह्मAPIHandler.routes[path] = response

    # स्पष्ट नाम, ताकि GET और POST अलग-अलग पढ़े जा सकें
    मार्ग_जोड़ें_GET = मार्ग_जोड़ें

    def मार्ग_जोड़ें_POST(self, path, handler):
        ब्रह्मAPIHandler.post_routes[path] = handler

    def प्रारम्भ(self):
        """सर्वर को पृष्ठभूमि थ्रेड में शुरू करें।"""
        if self.thread is not None and self.thread.is_alive():
            return self.thread
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.thread

    # वर्तनी भिन्नता (anusvara) के लिए alias
    प्रारंभ = प्रारम्भ

    def बन्द(self):
        """सर्वर बंद करें।"""
        self.server.shutdown()
        self.server.server_close()
        if self.thread is not None:
            self.thread.join(timeout=5)
        self.thread = None
