"""A tiny, dependency-free web framework used by the demo backends.

The generated demo applications originally depended on Flask, which is not
declared anywhere and therefore failed to import.  This module provides the
small subset those applications need — routing, JSON in/out, query strings,
headers, error handling — on top of the standard library only, and it never
opens a socket merely because a module was imported.

Example
-------
>>> from brahma_web import App, Request
>>> app = App("demo")
>>> @app.route("/status")
... def status(request):
...     return {"status": "ok"}
>>> response = app.handle(Request("GET", "/status"))
>>> response.status, response.payload
(200, {'status': 'ok'})
"""

from __future__ import annotations

import json
import re
import threading
import urllib.parse
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple

__all__ = ["App", "Request", "Response", "json_response", "text_response", "DEFAULT_PORT"]

DEFAULT_PORT = 8000


@dataclass
class Request:
    """A parsed HTTP request (also used directly in tests)."""

    method: str = "GET"
    path: str = "/"
    query: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    raw_body: bytes = b""

    def header(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Case-insensitive header lookup."""
        lowered = name.lower()
        for key, value in self.headers.items():
            if key.lower() == lowered:
                return value
        return default

    def json(self) -> Dict[str, Any]:
        """Return the parsed JSON body (``{}`` when there is none)."""
        if isinstance(self.body, dict):
            return self.body
        if not self.raw_body:
            return {}
        try:
            parsed = json.loads(self.raw_body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise BadRequest("invalid JSON body: %s" % exc)
        if not isinstance(parsed, dict):
            raise BadRequest("JSON body must be an object")
        return parsed

    @classmethod
    def parse(cls, method: str, target: str, headers, raw_body: bytes) -> "Request":
        parsed = urllib.parse.urlparse(target)
        query = {k: v[-1] for k, v in urllib.parse.parse_qs(parsed.query).items()}
        return cls(
            method=method.upper(),
            path=parsed.path or "/",
            query=query,
            headers=dict(headers or {}),
            raw_body=raw_body or b"",
        )


@dataclass
class Response:
    """An HTTP response."""

    status: int = 200
    payload: Any = None
    content_type: str = "application/json; charset=utf-8"
    headers: Dict[str, str] = field(default_factory=dict)

    def body_bytes(self) -> bytes:
        if isinstance(self.payload, (dict, list)):
            return json.dumps(self.payload, ensure_ascii=False).encode("utf-8")
        if isinstance(self.payload, bytes):
            return self.payload
        if self.payload is None:
            return b""
        return str(self.payload).encode("utf-8")


class BadRequest(Exception):
    """Raised by handlers to return HTTP 400."""

    status = 400


class Unauthorized(Exception):
    """Raised by handlers to return HTTP 401."""

    status = 401


class NotFound(Exception):
    """Raised by handlers to return HTTP 404."""

    status = 404


def json_response(payload: Any, status: int = 200) -> Response:
    """Build a JSON :class:`Response`."""
    return Response(status=status, payload=payload)


def text_response(text: str, status: int = 200) -> Response:
    """Build a ``text/plain`` :class:`Response`."""
    return Response(status=status, payload=text, content_type="text/plain; charset=utf-8")


_PARAM = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


class App:
    """A route table that can be served over HTTP."""

    def __init__(self, name: str = "app") -> None:
        self.name = name
        self.routes: List[Tuple[str, str, Callable, Tuple[str, ...]]] = []
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    # -- routing ---------------------------------------------------------
    def route(self, path: str, methods: Tuple[str, ...] = ("GET",)):
        """Decorator (or direct call) registering a handler for ``path``."""

        def register(handler: Callable) -> Callable:
            self.add(path, handler, methods)
            return handler

        return register

    def add(self, path: str, handler: Callable, methods: Tuple[str, ...] = ("GET",)) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        pattern = "^" + _PARAM.sub(r"(?P<\1>[^/]+)", path.rstrip("/") or "/") + "$"
        self.routes.append((path, pattern, handler, tuple(m.upper() for m in methods)))

    def _match(self, method: str, path: str):
        path = path.rstrip("/") or "/"
        allowed = set()
        for _, pattern, handler, methods in self.routes:
            match = re.match(pattern, path)
            if not match:
                continue
            if method not in methods:
                allowed.update(methods)
                continue
            return handler, match.groupdict()
        if allowed:
            raise _MethodNotAllowed(sorted(allowed))
        return None, {}

    # -- dispatch --------------------------------------------------------
    def handle(self, request: Request) -> Response:
        """Dispatch a :class:`Request` and always return a :class:`Response`."""
        try:
            handler, params = self._match(request.method, request.path)
        except _MethodNotAllowed as exc:
            return Response(
                status=405,
                payload={"status": "error", "message": "method not allowed", "allowed": exc.allowed},
            )
        if handler is None:
            return Response(status=404, payload={"status": "error", "message": "route not found"})

        try:
            result = handler(request, **params) if params else handler(request)
        except (BadRequest, Unauthorized, NotFound) as exc:
            return Response(status=exc.status, payload={"status": "error", "message": str(exc)})
        except KeyError as exc:
            return Response(
                status=400,
                payload={"status": "error", "message": "missing field: %s" % exc.args[0]},
            )
        except Exception as exc:  # noqa: BLE001 - never leak a traceback to a client
            return Response(
                status=500,
                payload={"status": "error", "message": "%s: %s" % (type(exc).__name__, exc)},
            )

        if isinstance(result, Response):
            return result
        if isinstance(result, dict) or isinstance(result, list):
            return Response(status=200, payload=result)
        return text_response(str(result))

    # -- serving ---------------------------------------------------------
    def make_handler(self):
        """Build a :class:`http.server.BaseHTTPRequestHandler` subclass."""
        app = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "BrahmaWeb/1.0"
            protocol_version = "HTTP/1.1"

            def log_message(self, fmt, *args):  # noqa: A003 - stdlib signature
                return  # keep demo output clean; enable via App(verbose=True)

            def _dispatch(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                request = Request.parse(self.command, self.path, self.headers, raw)
                response = app.handle(request)
                body = response.body_bytes()
                self.send_response(response.status)
                self.send_header("Content-Type", response.content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                for key, value in response.headers.items():
                    # HTTP header values are latin-1, but a handler may want to
                    # report a Devanagari value (e.g. an origin tag).  Escape
                    # anything outside latin-1 instead of killing the request.
                    safe = str(value)
                    try:
                        safe.encode("latin-1")
                    except UnicodeEncodeError:
                        safe = safe.encode("unicode_escape").decode("ascii")
                    self.send_header(key, safe)
                self.end_headers()
                if body:
                    self.wfile.write(body)

            do_GET = _dispatch
            do_POST = _dispatch
            do_PUT = _dispatch
            do_DELETE = _dispatch

            def do_OPTIONS(self):  # CORS preflight
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, token")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
                self.send_header("Content-Length", "0")
                self.end_headers()

        return Handler

    def bind(self, host: str = "0.0.0.0", port: int = DEFAULT_PORT) -> int:
        """Create the server socket; return the port actually bound."""
        self._server = ThreadingHTTPServer((host, port), self.make_handler())
        return self._server.server_address[1]

    def serve(self, host: str = "0.0.0.0", port: int = DEFAULT_PORT) -> None:
        """Bind and serve forever (blocking)."""
        port = self.bind(host, port)
        print("🕉️ %s सर्वर सक्रिय: http://%s:%d" % (self.name, host, port))
        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

    def start(self, host: str = "127.0.0.1", port: int = 0) -> int:
        """Bind and serve in a background thread; return the port."""
        port = self.bind(host, port)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return port

    def shutdown(self) -> None:
        """Stop the server and release the port."""
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None


class _MethodNotAllowed(Exception):
    def __init__(self, allowed: List[str]) -> None:
        super().__init__("method not allowed")
        self.allowed = allowed
