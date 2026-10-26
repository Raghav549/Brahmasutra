"""ब्रह्म स्वचालित निष्पादन API — सुरक्षित, केवल मानक लाइब्रेरी।

पहले यह सर्वर ``POST /run`` पर ग्राहक द्वारा दिया गया कोई भी अनुप्रयोग
``exec(code, globals())`` से सर्वर की अपनी प्रक्रिया में चला देता था, और
``app`` नाम की कोई जाँच नहीं थी (``../../`` से पथ-भेद संभव)। यानी यह एक खुला
रिमोट-कोड-निष्पादन द्वार था।

अब:

* नाम केवल सरल फ़ाइल-नाम हो सकता है (कोई ``/``, ``\\`` या ``..`` नहीं);
* चलाई जाने वाली फ़ाइल अनुप्रयोग-निर्देशिका के *भीतर* होनी चाहिए;
* अनुप्रयोग अलग उप-प्रक्रिया में, समय-सीमा और सीमित आउटपुट के साथ चलता है —
  सर्वर प्रक्रिया में कभी ``exec`` नहीं होता;
* निष्पादन केवल तब खुलता है जब ``BRAHMA_ALLOW_EXEC=1`` सेट हो (डिफ़ॉल्ट बंद).

एंडपॉइंट: ``GET /status`` और ``POST /run {"app": "नाम.py"}``।
"""

import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
while not os.path.exists(os.path.join(_ROOT, "brahma_web.py")):
    _parent = os.path.dirname(_ROOT)
    if _parent == _ROOT:
        raise ImportError("brahma_web.py नहीं मिला — रिपॉज़िटरी रूट से चलाएँ")
    _ROOT = _parent
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from brahma_web import App, BadRequest, text_response  # noqa: E402

DEFAULT_ROOT = os.path.join(_ROOT, "ब्रह्म_स्थापित")
TIMEOUT = 15
MAX_OUTPUT = 8192


def safe_app_path(root, name):
    """``root`` के भीतर रहने वाला पथ लौटाएँ, वरना :class:`BadRequest`।

    >>> safe_app_path('/srv/apps', 'demo.py')
    '/srv/apps/demo.py'
    >>> safe_app_path('/srv/apps', '../../etc/passwd')
    Traceback (most recent call last):
    brahma_web.BadRequest: invalid app name
    """
    if not isinstance(name, str) or not name.strip():
        raise BadRequest("app name required")
    if name != os.path.basename(name) or name.startswith(".") or os.sep in name or (os.altsep and os.altsep in name):
        raise BadRequest("invalid app name")
    root = os.path.abspath(root)
    path = os.path.abspath(os.path.join(root, name))
    if os.path.commonpath([root, path]) != root:
        raise BadRequest("app path escapes the application directory")
    if not os.path.isfile(path):
        raise BadRequest("app not found")
    return path


def exec_enabled():
    return os.environ.get("BRAHMA_ALLOW_EXEC") == "1"


def create_app(root=None):
    """निष्पादन API बनाएँ (सॉकेट नहीं खुलता)।"""
    installed = os.path.abspath(root or os.environ.get("BRAHMA_APPS_DIR") or DEFAULT_ROOT)
    app = App("ब्रह्म स्वचालित निष्पादन")

    @app.route("/")
    @app.route("/status")
    def status(_request):
        return {
            "status": "RUNNING",
            "engine": "BRAHMA",
            "exec_enabled": exec_enabled(),
            "apps_dir": installed,
        }

    @app.route("/apps")
    def apps(_request):
        if not os.path.isdir(installed):
            return {"apps": []}
        return {"apps": sorted(n for n in os.listdir(installed) if n.endswith((".py", ".सूत्र")))}

    @app.route("/run", methods=("POST",))
    def run_app(request):
        if not exec_enabled():
            raise BadRequest("execution is disabled; set BRAHMA_ALLOW_EXEC=1 to enable")
        name = request.json().get("app")
        path = safe_app_path(installed, name)
        try:
            completed = subprocess.run(
                [sys.executable, path],
                cwd=installed,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=TIMEOUT,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "app": name, "timeout": TIMEOUT}
        output = completed.stdout.decode("utf-8", "replace")[-MAX_OUTPUT:]
        return {
            "status": "success" if completed.returncode == 0 else "error",
            "app": name,
            "returncode": completed.returncode,
            "output": output,
        }

    return app


def main(argv=None):
    """सर्वर चलाएँ।"""
    import argparse

    parser = argparse.ArgumentParser(description="ब्रह्म स्वचालित निष्पादन API")
    parser.add_argument("--host", default=os.environ.get("BRAHMA_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=7005)
    parser.add_argument("--apps-dir", default=None)
    parser.add_argument("--once", action="store_true", help="पोर्ट बाँधकर तुरंत बंद करें")
    args = parser.parse_args(argv)

    api = create_app(args.apps_dir)
    if args.once:
        port = api.start(args.host, args.port)
        api.shutdown()
        print("🕉️ %d पोर्ट पर निष्पादन API तैयार (exec=%s)" % (port, exec_enabled()))
        return 0

    api.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
