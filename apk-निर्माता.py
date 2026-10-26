import os
import sys
import shutil


def apk_निर्माण(नाम):

    base = os.getcwd()

    output = os.path.join(base, "output")

    if not os.path.exists(output):
        os.mkdir(output)


    apk_path = os.path.join(output, नाम + ".apk")


    with open(apk_path, "w", encoding="utf-8") as f:

        f.write("संस्कृत APK\n")
        f.write("नाम: " + नाम + "\n")
        f.write("निर्माता: सूत्र भाषा\n")


    print("APK निर्मित:", apk_path)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    if len(sys.argv) < 2:

        print("उपयोग: python apk-निर्माता.py नाम")

    else:

        apk_निर्माण(sys.argv[1])


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
