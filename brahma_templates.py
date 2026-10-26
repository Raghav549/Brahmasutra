"""Code templates for the app generators.

The generators in this repository (``ब्रह्म_AI_बैकएंड_निर्माता.py`` and friends)
used to emit Flask applications.  Flask is not a dependency of this project, so
every application they produced failed at import with ``ModuleNotFoundError``.

The templates here are **self-contained**: a generated app only needs the
Python standard library, because it may be written to ``~/सूत्र-तंत्र/...``
outside this repository where ``brahma_web`` is not importable.

>>> "ThreadingHTTPServer" in CHAT_SERVER
True
"""

from __future__ import annotations

import os
from typing import Any, Dict

__all__ = ["CHAT_SERVER", "STATUS_SERVER", "write_chat_server", "write_status_server"]

_HEADER = '''"""{{title}}

यह सर्वर केवल Python मानक लाइब्रेरी से चलता है (कोई Flask आवश्यकता नहीं)।
आयात करने पर कुछ नहीं होता; केवल चलाने पर पोर्ट खुलता है।

चलाएँ::

    python {{filename}} --port {{port}}
"""

import argparse
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

'''


CHAT_SERVER = (
    _HEADER.replace("{{title}}", "ब्रह्म चैट सर्वर").replace("{{filename}}", "server.py")
    + '''USERS = {}
TOKENS = {}
CHAT = []

ROUTES = {}


def route(path, methods=("GET",)):
    def register(handler):
        pattern = "^" + re.sub(r"\\{(\\w+)\\}", r"(?P<\\1>[^/]+)", path) + "$"
        ROUTES[pattern] = (handler, tuple(m.upper() for m in methods))
        return handler

    return register


def dispatch(method, path, body):
    for pattern, (handler, methods) in ROUTES.items():
        match = re.match(pattern, path)
        if not match:
            continue
        if method not in methods:
            return 405, {"status": "error", "message": "method not allowed"}
        try:
            return 200, handler(body, **match.groupdict())
        except KeyError as exc:
            return 400, {"status": "error", "message": "missing field: %s" % exc.args[0]}
        except ValueError as exc:
            return 400, {"status": "error", "message": str(exc)}
    return 404, {"status": "error", "message": "route not found"}


@route("/")
@route("/status")
def status(_body):
    return {"status": "RUNNING", "app": "{{app_name}}"}


@route("/register", methods=("POST",))
def register(body):
    if not body.get("username") or not body.get("password"):
        raise ValueError("username and password are required")
    if body["username"] in USERS:
        return {"status": "exists"}
    USERS[body["username"]] = body["password"]
    return {"status": "registered"}


@route("/login", methods=("POST",))
def login(body):
    if USERS.get(body.get("username")) != body.get("password"):
        return {"status": "fail"}
    token = "tok-%d" % (len(TOKENS) + 1)
    TOKENS[token] = body["username"]
    return {"status": "ok", "token": token}


@route("/dashboard")
def dashboard(_body):
    return {"dashboard": "active", "users": len(USERS)}


@route("/send", methods=("POST",))
def send(body):
    if not body.get("msg"):
        raise ValueError("msg is required")
    CHAT.append({"user": body.get("user", "अतिथि"), "msg": body["msg"]})
    return {"status": "sent"}


@route("/chat")
def chat(_body):
    return {"messages": CHAT}


def make_handler():
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            return

        def _send(self, status_code, payload):
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            status_code, payload = dispatch("GET", self.path.split("?")[0], {})
            self._send(status_code, payload)

        def do_POST(self):
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except ValueError:
                self._send(400, {"status": "error", "message": "invalid JSON"})
                return
            status_code, payload = dispatch("POST", self.path.split("?")[0], body)
            self._send(status_code, payload)

        do_PUT = do_POST
        do_DELETE = do_POST

    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description="ब्रह्म चैट सर्वर")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7000)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), make_handler())
    print("🕉️ सर्वर सक्रिय: http://%s:%d" % (args.host, server.server_address[1]))
    if args.once:
        server.server_close()
        return 0
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
)

STATUS_SERVER = (
    _HEADER.replace("{{title}}", "ब्रह्म demo API").replace("{{filename}}", "api.py")
    + '''APP = "{{app_name}}"
ENGINE = "BRAHMA"


def payload():
    """वही JSON जो पहले Flask का ``/api`` लौटाता था।"""
    return {"status": "running", "app": APP, "engine": ENGINE}


def make_handler():
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            return

        def do_GET(self):
            data = json.dumps(payload(), ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)

    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description="ब्रह्म demo API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), make_handler())
    print("🕉️ API सक्रिय: http://%s:%d" % (args.host, server.server_address[1]))
    if args.once:
        server.server_close()
        return 0
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
)


def write_chat_server(directory: str, app_name: str = "brahma app") -> str:
    """Write a self-contained chat server into ``directory``; return its path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "server.py")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(CHAT_SERVER.replace("{{app_name}}", app_name))
    return path


def write_status_server(directory: str, app_name: str = "brahma app") -> str:
    """Write a self-contained status API into ``directory``; return its path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "api.py")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(STATUS_SERVER.replace("{{app_name}}", app_name))
    return path
