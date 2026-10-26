"""API तंत्र का लघु परीक्षण।

सर्वर पृष्ठभूमि थ्रेड में चलता है। जब इसे इंटरैक्टिव रूप से चलाया जाता है तो
Enter दबाने पर बंद होता है; स्वचालित (non-tty) रूप से चलाने पर तुरंत बंद हो
जाता है, ताकि CI अटके नहीं।
"""

import sys

from ब्रह्म_API_निष्पादन_तंत्र import ब्रह्मAPIनिष्पादनतंत्र


def test_get():
    return {"status": "GET working"}


def test_post(data):
    return {"status": "POST working", "received": data}


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global api

    api = ब्रह्मAPIनिष्पादनतंत्र(9100)


    api.मार्ग_जोड़ें_GET("/test", test_get)
    api.मार्ग_जोड़ें_POST("/send", test_post)
    api.प्रारम्भ()
    print("मार्ग: GET /test, POST /send")
    try:
        input("बंद करने के लिए Enter दबाएँ...")
    except EOFError:
        pass
    finally:
        api.बन्द()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
