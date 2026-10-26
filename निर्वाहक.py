# सूत्र तंत्र — निर्वाहक

from व्याकरणविश्लेषक import विश्लेषण

स्मृति = {}


def निर्वाह(पंक्ति):

    परिणाम = विश्लेषण(पंक्ति)

    प्रकार = परिणाम["प्रकार"]

    if प्रकार == "संकल्प-निर्धारण":

        नाम = परिणाम["नाम"]
        मान = परिणाम["मान"]

        स्मृति[नाम] = मान

    elif पंक्ति.startswith("मुद्रय"):

        भाग = पंक्ति.split()

        if len(भाग) >= 2:

            नाम = भाग[1]

            if नाम in स्मृति:

                print(स्मृति[नाम])

            else:

                print("अज्ञात संकल्प")

    else:

        print("अज्ञात आदेश")


def परीक्षण():

    print("सूत्र निर्वाहक सक्रिय")

    कोड१ = "संकल्प संख्या = १०"
    कोड२ = "मुद्रय संख्या"

    निर्वाह(कोड१)
    निर्वाह(कोड२)


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
