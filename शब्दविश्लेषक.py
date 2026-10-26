# सूत्र तंत्र — शब्द-विश्लेषक

from वर्णकोश import वर्ण_मान्य


def शब्द_विभाजन(पंक्ति):

    शब्दसूची = []
    वर्तमान_शब्द = ""

    for चिह्न in पंक्ति:

        if चिह्न == " " or चिह्न == "\n":

            if वर्तमान_शब्द != "":
                शब्दसूची.append(वर्तमान_शब्द)
                वर्तमान_शब्द = ""

        else:
            वर्तमान_शब्द += चिह्न

    if वर्तमान_शब्द != "":
        शब्दसूची.append(वर्तमान_शब्द)

    return शब्दसूची


def परीक्षण():

    print("सूत्र शब्द-विश्लेषक सक्रिय")

    कोड = "संकल्प संख्या = १०"

    परिणाम = शब्द_विभाजन(कोड)

    print("इनपुट:", कोड)

    print("शब्द:")

    for शब्द in परिणाम:
        print(शब्द)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    परीक्षण()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
