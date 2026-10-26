# 🕉️ ब्रह्म शब्द कोर VERSION 2


from ब्रह्म_वर्ण_कोर import ब्रह्मवर्णकोर


class ब्रह्मशब्दकोर:

    def __init__(self):

        self.वर्णकोर = ब्रह्मवर्णकोर()

    # शब्द valid है या नहीं
    def मान्य(self, शब्द):

        if शब्द == "":
            return False

        for वर्ण in शब्द:

            if not self.वर्णकोर.मान्य(वर्ण):
                return False

        return True

    # शब्द को वर्ण में विभाजित करो
    def विभाजित(self, शब्द):

        वर्णसूची = []

        for वर्ण in शब्द:

            वर्णसूची.append(वर्ण)

        return वर्णसूची

    # शब्द विश्लेषण
    def विश्लेषण(self, शब्द):

        if not self.मान्य(शब्द):

            return {
                "शब्द": शब्द,
                "मान्य": False,
                "लम्बाई": 0,
                "वर्ण": []
            }

        return {
            "शब्द": शब्द,
            "मान्य": True,
            "लम्बाई": len(शब्द),
            "वर्ण": self.विभाजित(शब्द)
        }


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global कोर, परिणाम, परीक्षण, शब्द
    print("🕉️ ब्रह्म शब्द कोर सक्रिय")
    कोर = ब्रह्मशब्दकोर()

    परीक्षण = [
        "अग्नि",
        "ब्रह्म",
        "कर्म",
        "ज्ञान",
        "APP"
    ]

    for शब्द in परीक्षण:

        परिणाम = कोर.विश्लेषण(शब्द)

        print("-----")
        print("शब्द:", परिणाम["शब्द"])
        print("मान्य:", परिणाम["मान्य"])
        print("लम्बाई:", परिणाम["लम्बाई"])
        print("वर्ण:", परिणाम["वर्ण"])


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
