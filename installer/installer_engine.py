import os
import shutil

FILES = [
    "engine",
    "compiler",
    "apk_build",
    "installer"
]

def install():
    print("संस्कृत प्रणाली स्थापना आरंभ...")

    if not os.path.exists(INSTALL_PATH):
        os.makedirs(INSTALL_PATH)

    base = os.path.expanduser("~/सूत्र-तंत्र")

    for folder in FILES:
        src = os.path.join(base, folder)
        dst = os.path.join(INSTALL_PATH, folder)

        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"{folder} स्थापित")

    print("पूर्ण स्थापना सफल")


INSTALL_PATH = os.path.expanduser("~/सूत्र-सिस्टम")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    install()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
