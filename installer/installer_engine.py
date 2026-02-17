import os
import shutil

INSTALL_PATH = os.path.expanduser("~/सूत्र-सिस्टम")

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

if __name__ == "__main__":
    install()
