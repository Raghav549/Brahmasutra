"""Shared chat/authentication backend used by the generated demo applications.

The generated demos (``ब्रह्म_AI_अनुप्रयोग/*/backend/server.py``) were eight
near-identical copies of the same Flask file with three problems the audit
flagged:

* Flask was an undeclared dependency, so none of them could start;
* passwords were stored in clear text;
* an administrator password (``admin123``) was hard-coded and committed.

This module replaces them with one implementation:

* standard library only (:mod:`brahma_web` + :mod:`hashlib` + :mod:`json`);
* PBKDF2-HMAC-SHA256 password hashes with a per-user salt;
* the administrator password comes from ``BRAHMA_ADMIN_PASSWORD`` or, when it
  is absent, is generated at start-up and printed once;
* atomic JSON writes, so a crash cannot truncate the user database;
* an import-safe module: the server socket is only created by ``main()``;
* the ब्रह्म-LLM is exposed on the same app (``/llm``, ``/llm/generate``,
  ``/llm/run``), so a chat client and the language model share one server.

Run one of the demos with::

    python ब्रह्म_AI_अनुप्रयोग/chat_app/backend/server.py --port 9000
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import secrets
import sys
import tempfile
from typing import Any, Dict, List, Optional

from brahma_web import App, BadRequest, Request, Unauthorized

__all__ = ["Store", "create_app", "main"]

PBKDF2_ROUNDS = 120_000
DEFAULT_DATA_DIR = os.environ.get("BRAHMA_DATA_DIR") or os.path.join(
    tempfile.gettempdir(), "brahma-chat"
)


# ---------------------------------------------------------------------------
# storage
# ---------------------------------------------------------------------------
class Store:
    """Tiny JSON-backed store with atomic writes."""

    def __init__(self, data_dir: Optional[str] = None) -> None:
        self.data_dir = os.path.abspath(data_dir or DEFAULT_DATA_DIR)
        os.makedirs(self.data_dir, exist_ok=True)
        self.users_path = os.path.join(self.data_dir, "users.json")
        self.chat_path = os.path.join(self.data_dir, "chat.json")
        if not os.path.exists(self.users_path):
            self._write(self.users_path, {})
        if not os.path.exists(self.chat_path):
            self._write(self.chat_path, [])

    # -- io --------------------------------------------------------------
    @staticmethod
    def _read(path: str, default):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            return default

    @staticmethod
    def _write(path: str, data) -> None:
        directory = os.path.dirname(path)
        handle = tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=directory, delete=False, suffix=".tmp"
        )
        try:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            handle.close()
        os.replace(handle.name, path)

    # -- users -----------------------------------------------------------
    def users(self) -> Dict[str, Dict[str, str]]:
        data = self._read(self.users_path, {})
        return data if isinstance(data, dict) else {}

    def has_user(self, username: str) -> bool:
        return username in self.users()

    def add_user(self, username: str, password: str) -> None:
        users = self.users()
        salt = secrets.token_hex(16)
        users[username] = {"salt": salt, "hash": _hash(password, salt)}
        self._write(self.users_path, users)

    def delete_user(self, username: str) -> bool:
        users = self.users()
        if username not in users:
            return False
        del users[username]
        self._write(self.users_path, users)
        return True

    def check_password(self, username: str, password: str) -> bool:
        record = self.users().get(username)
        if not isinstance(record, dict):
            return False
        expected = record.get("hash", "")
        actual = _hash(password, record.get("salt", ""))
        return hmac.compare_digest(expected, actual)

    # -- chat ------------------------------------------------------------
    def messages(self) -> List[Dict[str, Any]]:
        data = self._read(self.chat_path, [])
        return data if isinstance(data, list) else []

    def add_message(self, user: str, message: str) -> None:
        chat = self.messages()
        chat.append({"user": user, "msg": message})
        self._write(self.chat_path, chat)


def _hash(password: str, salt: str) -> str:
    if not isinstance(password, str):
        raise BadRequest("password must be a string")
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ROUNDS
    ).hex()


# ---------------------------------------------------------------------------
# application
# ---------------------------------------------------------------------------
def create_app(
    name: str = "brahma chat",
    data_dir: Optional[str] = None,
    admin: bool = False,
    admin_password: Optional[str] = None,
    llm: bool = True,
    llm_dir: Optional[str] = None,
) -> App:
    """Build the chat application (no socket is opened here)."""
    store = Store(data_dir)
    tokens: Dict[str, str] = {}
    admin_tokens: Dict[str, str] = {}

    password = admin_password or os.environ.get("BRAHMA_ADMIN_PASSWORD")
    generated_password = False
    if admin and not password:
        password = secrets.token_urlsafe(9)
        generated_password = True

    app = App(name)

    # -- helpers ---------------------------------------------------------
    def require_user(request: Request) -> str:
        token = request.header("token") or request.query.get("token")
        if not token or token not in tokens:
            raise Unauthorized("valid token required")
        return tokens[token]

    def require_admin(request: Request) -> str:
        token = request.header("token") or request.query.get("token")
        if not token or token not in admin_tokens:
            raise Unauthorized("administrator token required")
        return admin_tokens[token]

    def credentials(request: Request):
        body = request.json()
        username = body.get("username")
        password_value = body.get("password")
        if not username or not password_value:
            raise BadRequest("username and password are required")
        if not isinstance(username, str) or not isinstance(password_value, str):
            raise BadRequest("username and password must be strings")
        if len(username) > 64 or len(password_value) > 256:
            raise BadRequest("username or password too long")
        return username, password_value

    # -- routes ----------------------------------------------------------
    @app.route("/")
    @app.route("/status")
    def status(_request: Request):
        return {"status": "RUNNING", "app": name}

    @app.route("/register", methods=("POST",))
    def register(request: Request):
        username, password_value = credentials(request)
        if store.has_user(username):
            return {"status": "exists"}
        store.add_user(username, password_value)
        return {"status": "ok"}

    @app.route("/login", methods=("POST",))
    def login(request: Request):
        username, password_value = credentials(request)
        if store.check_password(username, password_value):
            token = secrets.token_urlsafe(24)
            tokens[token] = username
            return {"status": "ok", "token": token}
        return {"status": "fail"}

    @app.route("/dashboard")
    def dashboard(request: Request):
        return {"status": "ok", "user": require_user(request)}

    @app.route("/send", methods=("POST",))
    def send(request: Request):
        user = require_user(request)
        message = request.json().get("msg")
        if not message or not isinstance(message, str):
            raise BadRequest("msg is required")
        store.add_message(user, message)
        return {"status": "sent"}

    @app.route("/chat")
    def chat(_request: Request):
        return {"messages": store.messages()}

    # -- ब्रह्म-LLM -------------------------------------------------------
    # Loaded lazily and cached: importing a chat server must not pay for the
    # model, and a missing checkpoint is reported instead of crashing.
    model_cache: Dict[str, Any] = {}

    def get_model():
        if "model" in model_cache:
            return model_cache["model"]
        try:
            from brahma_llm.model import BrahmaLLM
        except ImportError:
            model_cache["model"] = None
            model_cache["error"] = "brahma_llm उपलब्ध नहीं"
            return None
        directory = llm_dir
        if directory is None:
            try:
                from brahma_paths import data_root

                directory = data_root("llm", "best")
            except ImportError:  # pragma: no cover - brahma_paths always ships
                directory = ""
        if not directory or not os.path.isdir(directory):
            model_cache["model"] = None
            model_cache["error"] = "कोई चेकपॉइंट नहीं (brahma llm train चलाएँ)"
            return None
        try:
            model_cache["model"] = BrahmaLLM.load(directory)
        except (OSError, ValueError, KeyError) as error:
            model_cache["model"] = None
            model_cache["error"] = "चेकपॉइंट पढ़ा नहीं जा सका: %s" % error
            return None
        return model_cache["model"]

    if llm:

        @app.route("/llm")
        def llm_status(_request: Request):
            model = get_model()
            if model is None:
                return {"available": False, "reason": model_cache.get("error", "")}
            info = model.info()
            return {"available": True, "kind": info["kind"], "size": info["size"],
                    "params": info["params"], "vocab": info["vocab_size"]}

        @app.route("/llm/generate", methods=("POST",))
        def llm_generate(request: Request):
            model = get_model()
            if model is None:
                return {"status": "unavailable", "reason": model_cache.get("error", "")}
            body = request.json()
            prompt = body.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise BadRequest("prompt is required")
            if len(prompt) > 4000:
                raise BadRequest("prompt too long (max 4000 characters)")
            tokens = body.get("tokens", 60)
            temperature = body.get("temperature", 0.9)
            if not isinstance(tokens, int) or not 1 <= tokens <= 400:
                raise BadRequest("tokens must be an integer in 1..400")
            if not isinstance(temperature, (int, float)) or not 0.0 <= float(temperature) <= 2.0:
                raise BadRequest("temperature must be in 0..2")
            text = model.generate(prompt, max_tokens=tokens, temperature=float(temperature))
            return {"status": "ok", "text": text, "params": model.model.parameter_count()}

        @app.route("/llm/run", methods=("POST",))
        def llm_run(request: Request):
            """Compile and run सूत्र source posted by the client (sandboxed)."""
            from brahma.api import execute

            body = request.json()
            source = body.get("source")
            if not isinstance(source, str) or not source.strip():
                raise BadRequest("source is required")
            if len(source) > 20_000:
                raise BadRequest("source too long (max 20000 characters)")
            result = execute(source, source_name="<http>", step_limit=100_000)
            return {"ok": result.error is None, "output": result.output,
                    "error": None if result.error is None else str(result.error),
                    "steps": result.steps}

    if admin:

        @app.route("/admin_login", methods=("POST",))
        def admin_login(request: Request):
            username, password_value = credentials(request)
            admin_user = os.environ.get("BRAHMA_ADMIN_USER", "admin")
            if username == admin_user and hmac.compare_digest(password_value, password or ""):
                token = secrets.token_urlsafe(24)
                admin_tokens[token] = username
                return {"status": "ok", "token": token}
            return {"status": "fail"}

        @app.route("/users")
        def users(request: Request):
            require_admin(request)
            return {"users": sorted(store.users())}

        @app.route("/delete_user", methods=("POST",))
        def delete_user(request: Request):
            require_admin(request)
            username = request.json().get("username")
            if not username:
                raise BadRequest("username is required")
            return {"status": "deleted" if store.delete_user(username) else "missing"}

        if generated_password:  # pragma: no cover - printed once at start-up
            app.admin_password = password

    return app


def main(argv: Optional[List[str]] = None, default_port: int = 9000, admin: bool = False) -> int:
    """CLI entry point shared by the demo servers."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=os.environ.get("BRAHMA_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("BRAHMA_PORT", default_port)))
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--once", action="store_true", help="bound the port, print the URL and exit")
    args = parser.parse_args(argv)

    app = create_app(data_dir=args.data_dir, admin=admin)
    if args.once:
        port = app.start(args.host, args.port)
        app.shutdown()
        print("🕉️ %d पोर्ट पर सर्वर तैयार (--once)" % port)
        return 0

    password = getattr(app, "admin_password", None)
    if password:
        print("🔐 प्रशासक पासवर्ड (BRAHMA_ADMIN_PASSWORD सेट करें): %s" % password)
    try:
        app.serve(args.host, args.port)
    except OSError as exc:
        print("त्रुटि: सर्वर प्रारम्भ नहीं हो सका: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
