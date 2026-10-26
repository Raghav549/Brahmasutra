# सूत्र तंत्र — व्याकरण विश्लेषक

from शब्दविश्लेषक import शब्द_विभाजन


def विश्लेषण(पंक्ति):

    शब्दसूची = शब्द_विभाजन(पंक्ति)

    if len(शब्दसूची) >= 4:

        प्रथम = शब्दसूची[0]

        if प्रथम == "संकल्प":

            नाम = शब्दसूची[1]
            चिह्न = शब्दसूची[2]
            मान = शब्दसूची[3]

            if चिह्न == "=":

                return {
                    "प्रकार": "संकल्प-निर्धारण",
                    "नाम": नाम,
                    "मान": मान
                }

    return {
        "प्रकार": "अज्ञात"
    }


def परीक्षण():

    print("सूत्र व्याकरण-विश्लेषक सक्रिय")

    कोड = "संकल्प संख्या = १०"

    परिणाम = विश्लेषण(कोड)

    print("इनपुट:", कोड)

    print("विश्लेषण परिणाम:")

    for कुंजी in परिणाम:
        print(कुंजी, ":", परिणाम[कुंजी])


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
