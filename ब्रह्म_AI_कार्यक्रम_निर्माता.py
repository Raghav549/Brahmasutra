# 🕉️ ब्रह्म AI कार्यक्रम निर्माता
# संस्कृत कोड → executable कार्यक्रम


import os


class ब्रह्मकार्यक्रमनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म कार्यक्रम निर्माता सक्रिय")

        self.folder = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्रम")

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)


    def निर्मित(self, नाम, कोड):

        path = os.path.join(self.folder, नाम + ".ब्रह्म")

        with open(path, "w", encoding="utf-8") as f:

            f.write(कोड)

        print("कार्यक्रम निर्मित:", path)

        return path


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश, कार्यक्रमनिर्माता, कोड, कोडनिर्माता, नाम, विश्लेषक, संरचना
    from ब्रह्म_AI_विश्लेषक import ब्रह्मविश्लेषक
    from ब्रह्म_AI_कोड_निर्माता import ब्रह्मकोडनिर्माता

    विश्लेषक = ब्रह्मविश्लेषक()

    कोडनिर्माता = ब्रह्मकोडनिर्माता()

    कार्यक्रमनिर्माता = ब्रह्मकार्यक्रमनिर्माता()


    आदेश = input("आदेश लिखें: ")

    संरचना = विश्लेषक.विश्लेषण(आदेश)

    कोड = कोडनिर्माता.निर्मित(संरचना)


    नाम = संरचना["प्रकार"]

    कार्यक्रमनिर्माता.निर्मित(नाम, कोड)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
