"""ब्रह्म चैट सर्वर — केवल मानक लाइब्रेरी।

यह फ़ाइल पहले Flask + flask_cors पर निर्भर थी, जो कहीं घोषित नहीं थे, इसलिए
सर्वर कभी शुरू नहीं होता था। अब यह वही API :mod:`brahma_chat` (stdlib) से
परोसती है: /status /register /login /dashboard /send /chat

चलाएँ::

    python ब्रह्म_स्थापित/chat_app_with_login_database_api_dashboard/backend/server.py --port 9400
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


from brahma_chat import main as chat_main


def main(argv=None):
    """सर्वर चलाएँ (``--once`` से केवल पोर्ट बाँधकर जाँचें)।"""
    return chat_main(argv, default_port=9400, admin=False)


if __name__ == "__main__":
    raise SystemExit(main())
