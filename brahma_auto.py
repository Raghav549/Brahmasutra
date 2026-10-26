#!/usr/bin/env python3
"""ब्रह्म ऑटो जनरेटर — प्रॉम्प्ट से एक चलने योग्य अनुप्रयोग बनाएँ।

पहले यह स्क्रिप्ट आयात करते ही ``input()`` पर अटक जाती थी और जो ऐप बनाती थी
वह Flask पर निर्भर था (जो इस परियोजना में कहीं घोषित नहीं है)। अब:

* प्रॉम्प्ट कमांड-लाइन से लिया जाता है (``brahma_auto.py "मेरा ऐप"``);
* कोई प्रॉम्प्ट न हो और टर्मिनल भी न हो तो उपयोग-संदेश दिखाकर बाहर निकलता है
  (कभी अनंत प्रतीक्षा नहीं);
* बना हुआ बैकएंड केवल मानक लाइब्रेरी से चलता है (:mod:`brahma_templates`);
* कौन-सा टेम्पलेट बनेगा यह :class:`brahma_ai.PromptRouter` तय करता है — वह एक
  स्पष्ट कीवर्ड-नियम है (न्यूरल नेटवर्क नहीं) और ``--explain`` से दिखता है;
* ``--dry-run`` से केवल योजना दिखती है, कुछ नहीं लिखा जाता।

उदाहरण::

    python brahma_auto.py "मेरा चैट ऐप" --out /tmp/apps
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import unicodedata
from typing import List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from brahma_ai import PromptRouter  # noqa: E402
from brahma_templates import write_chat_server, write_status_server  # noqa: E402

DEFAULT_BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

FRONTEND = """<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ background: #0b0b0b; color: #9fef00; font-family: system-ui, sans-serif;
         text-align: center; padding: 2rem; }}
  input, button {{ font: inherit; padding: .5rem .75rem; margin: .25rem;
                   border-radius: .4rem; border: 1px solid #333; }}
  button {{ background: #9fef00; color: #111; cursor: pointer; }}
  pre {{ text-align: left; max-width: 40rem; margin: 1rem auto; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p>बैकएंड: <code>http://127.0.0.1:{port}</code></p>
<input id="u" placeholder="उपयोगकर्ता नाम">
<input id="p" placeholder="पासवर्ड" type="password">
<button onclick="register()">पंजीकरण</button>
<button onclick="login()">लॉगिन</button>
<button onclick="status()">स्थिति</button>
<pre id="out"></pre>
<script>
const API = "http://127.0.0.1:{port}";
let token = "";
const out = document.getElementById("out");
const post = (path, body) => fetch(API + path, {{
  method: "POST",
  headers: {{"Content-Type": "application/json", ...(token ? {{token}} : {{}})}},
  body: JSON.stringify(body || {{}})
}}).then(r => r.json()).then(show);
function show(data) {{ out.innerText = JSON.stringify(data, null, 2); }}
function register() {{ post("/register", {{username: u.value, password: p.value}}); }}
function login() {{ post("/login", {{username: u.value, password: p.value}})
  .then(d => {{ token = d.token || token; }}); }}
function status() {{ fetch(API + "/status").then(r => r.json()).then(show); }}
</script>
</body>
</html>
"""


def safe_app_name(prompt: str) -> str:
    """Turn a prompt into a safe directory name.

    >>> safe_app_name("मेरा चैट ऐप")
    'मेरा_चैट_ऐप'
    >>> safe_app_name("../../etc")
    'etc'
    """
    name = re.sub(r"\s+", "_", (prompt or "").strip())
    # keep letters, digits, Devanagari matras (Mn/Mc) and _ - .
    name = "".join(
        ch for ch in name
        if ch.isalnum() or ch in "_-." or unicodedata.category(ch) in ("Mn", "Mc")
    )
    name = name.replace("..", "").strip("._")
    return name or "brahma_app"


def create_app(prompt: str, base: Optional[str] = None, port: int = 9000,
               kind: Optional[str] = None, dry_run: bool = False) -> str:
    """Create an application directory for ``prompt``; return its path.

    ``kind`` defaults to the template chosen by :class:`brahma_ai.PromptRouter`
    (``chat`` / ``admin_chat`` → chat server, ``status`` → status API).
    """
    name = safe_app_name(prompt)
    template = PromptRouter().route(prompt) if kind is None else kind
    if template == "admin_chat":
        kind = "chat"
    elif template in ("chat", "status"):
        kind = template
    kind = kind or "chat"
    root = os.path.abspath(os.path.expanduser(base or DEFAULT_BASE))
    app_path = os.path.join(root, name)
    backend = os.path.join(app_path, "backend")
    frontend = os.path.join(app_path, "frontend")

    if dry_run:
        print("बनाया जाएगा:", app_path)
        print("  बैकएंड:", os.path.join(backend, "server.py" if kind == "chat" else "api.py"))
        print("  फ्रंटएंड:", os.path.join(frontend, "index.html"))
        return app_path

    if kind == "chat":
        write_chat_server(backend, name)
    else:
        write_status_server(backend, name)

    os.makedirs(frontend, exist_ok=True)
    with open(os.path.join(frontend, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(FRONTEND.format(title=html.escape(prompt or name), port=port))

    with open(os.path.join(app_path, "README.md"), "w", encoding="utf-8") as handle:
        handle.write(
            "# %s\n\n"
            "`brahma_auto.py` द्वारा निर्मित।\n\n"
            "```sh\npython backend/%s --port %d\n```\n\n"
            "फिर `frontend/index.html` ब्राउज़र में खोलें।\n"
            % (prompt or name, "server.py" if kind == "chat" else "api.py", port)
        )

    return app_path


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="ब्रह्म ऑटो जनरेटर")
    parser.add_argument("prompt", nargs="*", help="अनुप्रयोग का विवरण")
    parser.add_argument("--out", default=None, help="आधार निर्देशिका")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--kind", choices=("chat", "status"), default=None,
                        help="डिफ़ॉल्ट: brahma_ai.PromptRouter का चयन")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--explain", action="store_true",
                        help="दिखाएँ कि कौन-सा नियम लागू हुआ")
    args = parser.parse_args(argv)

    prompt = " ".join(args.prompt).strip()
    if not prompt:
        if sys.stdin is not None and sys.stdin.isatty():
            try:
                prompt = input("अनुप्रयोग का विवरण: ").strip()
            except EOFError:
                prompt = ""
        if not prompt:
            parser.print_usage(sys.stderr)
            print("त्रुटि: कृपया अनुप्रयोग का विवरण दें, जैसे: brahma_auto.py 'मेरा चैट ऐप'",
                  file=sys.stderr)
            return 2

    decision = PromptRouter().options(prompt)
    if args.explain:
        print(
            "टेम्पलेट: %s (नियम: %r) — विशेषताएँ: %s"
            % (decision["template"], decision["matched"], ", ".join(decision["features"]))
        )

    path = create_app(prompt, args.out, args.port, args.kind, args.dry_run)
    if not args.dry_run:
        print("APP CREATED:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
