"""ब्रह्म demo API — केवल मानक लाइब्रेरी।

ये endpoints पहले Flask से बनते थे; अब :mod:`brahma_web` (stdlib) उपयोग होता है।
सर्वर आयात के समय नहीं, केवल चलाने पर खुलता है।
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
while not os.path.exists(os.path.join(_ROOT, "brahma_chat.py")):
    _parent = os.path.dirname(_ROOT)
    if _parent == _ROOT:
        raise ImportError("brahma_chat.py नहीं मिला — रिपॉज़िटरी रूट से चलाएँ")
    _ROOT = _parent
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


from brahma_web import App


def create_app():
    """API ऐप बनाएँ।"""
    app = App("chat app with login database api dashboard")

    @app.route("/")
    @app.route("/api")
    def status(_request):
        return {"status": "running", "app": "chat app with login database api dashboard", "engine": "BRAHMA AI VERSION 36"}

    return app


def main(argv=None):
    """सर्वर चलाएँ।"""
    import argparse

    parser = argparse.ArgumentParser(description="ब्रह्म demo API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--once", action="store_true", help="पोर्ट बाँधकर तुरंत बंद करें")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args(argv)
    app = create_app()
    if args.once:
        port = app.start(args.host, args.port)
        app.shutdown()
        print("🕉️ %d पोर्ट पर API तैयार (--once)" % port)
        return 0

    app.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
