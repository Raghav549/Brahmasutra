"""🕉️ ब्रह्म AI API — a small JSON key/value store over HTTP.

The original version read ``Content-Length`` bytes without a bound, crashed on
malformed JSON, served from a hard-coded ``0.0.0.0:9000`` and rewrote the store
file in place (a crash could truncate it).  This rewrite uses :mod:`brahma_web`
and:

* caps request bodies at :data:`MAX_BODY`;
* answers ``400`` for bad JSON and ``413`` for oversized bodies;
* writes the store atomically (temp file + ``os.replace``);
* binds ``127.0.0.1`` unless ``--host`` says otherwise;
* supports ``--once`` so CI can smoke-test it without blocking.

Endpoints: ``GET /`` (all keys), ``GET /<key>``, ``POST /`` (merge an object),
``DELETE /<key>``, ``GET /status``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from brahma_web import App, BadRequest, Response  # noqa: E402

MAX_BODY = 1_000_000
BASE = os.environ.get("BRAHMA_AI_API_DIR") or os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_API")
DB = os.path.join(BASE, "data.db")


def load(path: str = None) -> dict:
    """Read the store (``{}`` when the file does not exist yet)."""
    path = path or DB
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {}
    except ValueError as exc:
        raise RuntimeError("data.db में अमान्य JSON: %s" % exc)
    return data if isinstance(data, dict) else {}


def save(data: dict, path: str = None) -> str:
    """Write the store atomically; return the path."""
    path = path or DB
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=os.path.dirname(os.path.abspath(path)),
        delete=False, suffix=".tmp",
    )
    try:
        json.dump(data, handle, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())
    finally:
        handle.close()
    os.replace(handle.name, path)
    return path


def create_app(db_path: str = None) -> App:
    """Build the API (no socket is opened)."""
    path = db_path or DB
    app = App("ब्रह्म AI API")

    @app.route("/")
    def सब(_request):
        return load(path)

    @app.route("/status")
    def status(_request):
        return {"status": "RUNNING", "keys": len(load(path))}

    @app.route("/{key}")
    def one(request, key):
        data = load(path)
        if key not in data:
            return Response(status=404, payload={"status": "error", "message": "key not found"})
        return {key: data[key]}

    @app.route("/{key}", methods=("DELETE",))
    def delete(request, key):
        data = load(path)
        if key not in data:
            return Response(status=404, payload={"status": "error", "message": "key not found"})
        del data[key]
        save(data, path)
        return {"status": "deleted", "key": key}

    @app.route("/", methods=("POST",))
    def store(request):
        if len(request.raw_body or b"") > MAX_BODY:
            return Response(status=413, payload={"status": "error", "message": "body too large"})
        payload = request.json()
        if not isinstance(payload, dict):
            raise BadRequest("body must be a JSON object")
        data = load(path)
        data.update(payload)
        save(data, path)
        return {"status": "saved", "keys": len(data)}

    return app


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ब्रह्म AI API")
    parser.add_argument("--host", default=os.environ.get("BRAHMA_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--data", default=DB)
    parser.add_argument("--once", action="store_true", help="पोर्ट बाँधकर तुरंत बंद करें")
    args = parser.parse_args(argv)

    os.makedirs(os.path.dirname(os.path.abspath(args.data)), exist_ok=True)
    if not os.path.exists(args.data):
        save({}, args.data)

    app = create_app(args.data)
    if args.once:
        port = app.start(args.host, args.port)
        app.shutdown()
        print("🕉️ API %d पोर्ट पर तैयार (--once)" % port)
        return 0

    print("🕉️ ब्रह्म AI API Engine सक्रिय — http://%s:%d" % (args.host, args.port))
    app.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
