import os
import shutil
DOWNLOAD = "/sdcard/Download"


def स्थापन(apk_name):

    source = os.path.join(BASE, "output", apk_name)

    if not os.path.exists(source):

        print("त्रुटि: APK नहीं मिला")
        return


    dest = os.path.join(DOWNLOAD, apk_name)

    shutil.copy(source, dest)


    print("APK Download folder में स्थापित:")
    print(dest)

    print("\nअब install करने हेतु:")
    print("File Manager → Download →", apk_name)


BASE = os.path.expanduser("~/सूत्र-तंत्र")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    pass


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
