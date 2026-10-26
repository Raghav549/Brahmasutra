# 🕉️ कुंजीपटल चालक (keyboard driver)
#
# Reads a line from stdin. When stdin is not a terminal (CI, cron, a piped
# demo) there is nothing to read, so the driver returns a harmless default
# instead of raising EOFError.

import sys


def कुंजीपटल_पठन(_=None, डिफ़ॉल्ट=""):
    try:
        if not sys.stdin or sys.stdin.closed:
            return डिफ़ॉल्ट
        if not sys.stdin.isatty():
            पंक्ति = sys.stdin.readline()
            return पंक्ति.rstrip("\n") if पंक्ति else डिफ़ॉल्ट
        return input("⌨️ इनपुट दें: ")
    except (EOFError, KeyboardInterrupt):
        return डिफ़ॉल्ट
