# 🕉️ सूत्र User Mode Controller


class सूत्रUserMode:


    def __init__(self):

        print("🕉️ User Mode सक्रिय")


    def execute_user_app(self, app):

        print("User app running:", app)


# ---------------------------------------------------------------------------
# Module level helpers used by ``सूत्र_mode_test.py``.
# ---------------------------------------------------------------------------
_वर्तमान = None


def प्रारम्भ():
    """Enter (or return) the current user-mode controller."""
    global _वर्तमान
    if _वर्तमान is None:
        _वर्तमान = सूत्रUserMode()
    return _वर्तमान


def ऐप_चलाओ(ऐप):
    return प्रारम्भ().execute_user_app(ऐप)


def प्रणाली_आह्वान(नाम):
    """Perform a system call from user mode.

    User mode may only read status; everything else is refused, which mirrors
    the privilege check in the kernel demo.
    """
    import सूत्र_आह्वान_तंत्र as आह्वान

    तंत्र = आह्वान.आह्वानतंत्र()
    if नाम in ("स्मृति_स्थिति", "यन्त्र_स्थिति", "स्थिति"):
        print(f"उपयोगकर्ता आह्वान अनुमत: {नाम}")
        return तंत्र.आह्वान("स्मृति", नाम)
    print(f"उपयोगकर्ता आह्वान अस्वीकृत: {नाम}")
    return None
