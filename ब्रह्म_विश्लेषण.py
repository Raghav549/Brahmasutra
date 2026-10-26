# 🕉️ BRAHMA TRUE AI ENGINE — VERSION 3 PROMPT ANALYSIS ENGINE



# ============================================
# ब्रह्म विश्लेषक
# ============================================

class ब्रह्मविश्लेषक:

    def __init__(self):

        print("ब्रह्म विश्लेषक सक्रिय")

        self.प्रकार = None

        self.घटक = []


    # ========================================
    # prompt विश्लेषण
    # ========================================

    def विश्लेषण(self, प्रवेश):

        प्रवेश = प्रवेश.lower()

        परिणाम = {

            "प्रकार": None,
            "घटक": []

        }


        # ====================================
        # प्रकार पहचान
        # ====================================

        if "app" in प्रवेश:

            परिणाम["प्रकार"] = "अनुप्रयोग"

        elif "website" in प्रवेश:

            परिणाम["प्रकार"] = "वेबसाइट"

        elif "ai" in प्रवेश:

            परिणाम["प्रकार"] = "कृत्रिमबुद्धि"

        elif "saas" in प्रवेश:

            परिणाम["प्रकार"] = "सास"

        else:

            परिणाम["प्रकार"] = "सामान्य"


        # ====================================
        # घटक पहचान
        # ====================================

        if "login" in प्रवेश:

            परिणाम["घटक"].append("प्रवेश प्रणाली")

        if "database" in प्रवेश:

            परिणाम["घटक"].append("संग्रह तंत्र")

        if "api" in प्रवेश:

            परिणाम["घटक"].append("एपीआई तंत्र")

        if "chat" in प्रवेश:

            परिणाम["घटक"].append("संवाद तंत्र")

        if "dashboard" in प्रवेश:

            परिणाम["घटक"].append("डैशबोर्ड")


        print("विश्लेषण परिणाम:")

        print("प्रकार:", परिणाम["प्रकार"])

        print("घटक:", परिणाम["घटक"])

        return परिणाम


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म विश्लेषण प्रणाली प्रारम्भ")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
