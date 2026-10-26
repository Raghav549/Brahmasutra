# 🕉️ ब्रह्म AI विश्लेषक तंत्र

class ब्रह्मविश्लेषक:

    def __init__(self):

        print("🕉️ ब्रह्म AI विश्लेषक सक्रिय")


    def विश्लेषण(self, आदेश):

        संरचना = {
            "प्रकार": None,
            "विशेषताएँ": []
        }

        आदेश = आदेश.lower()


        # प्रकार पहचान

        if "chat" in आदेश:
            संरचना["प्रकार"] = "chat_app"

        elif "website" in आदेश:
            संरचना["प्रकार"] = "website"

        elif "api" in आदेश:
            संरचना["प्रकार"] = "api"

        elif "tool" in आदेश:
            संरचना["प्रकार"] = "tool"

        else:
            संरचना["प्रकार"] = "general_app"


        # विशेषताएँ पहचान

        if "login" in आदेश:
            संरचना["विशेषताएँ"].append("login")

        if "database" in आदेश:
            संरचना["विशेषताएँ"].append("database")

        if "api" in आदेश:
            संरचना["विशेषताएँ"].append("api")

        if "ui" in आदेश:
            संरचना["विशेषताएँ"].append("ui")

        if "auth" in आदेश:
            संरचना["विशेषताएँ"].append("auth")

        if "dashboard" in आदेश:
            संरचना["विशेषताएँ"].append("dashboard")

        return संरचना


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश, परिणाम, विश्लेषक
    विश्लेषक = ब्रह्मविश्लेषक()

    आदेश = input("आदेश लिखें: ")

    परिणाम = विश्लेषक.विश्लेषण(आदेश)

    print("\nसंरचना:")
    print("प्रकार:", परिणाम["प्रकार"])
    print("विशेषताएँ:", परिणाम["विशेषताएँ"])


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
