import os
import shutil

BASE = os.path.expanduser("~/सूत्र-तंत्र/store/apps")

def सूची():

    apps = os.listdir(BASE)

    if not apps:
        print("कोई अनुप्रयोग उपलब्ध नहीं")
        return

    print("उपलब्ध अनुप्रयोग:\n")

    for i, app in enumerate(apps, 1):
        print(f"{i}. {app}")

def प्रकाशित(apk):

    if not os.path.exists(apk):
        print("APK नहीं मिला")
        return

    name = os.path.basename(apk)

    dest = os.path.join(BASE, name)

    shutil.copy(apk, dest)

    print("अनुप्रयोग प्रकाशित:")
    print(name)

def संस्थापन(name):

    path = os.path.join(BASE, name)

    if not os.path.exists(path):
        print("अनुप्रयोग नहीं मिला")
        return

    dest = "/sdcard/Download/" + name

    shutil.copy(path, dest)

    print("अनुप्रयोग स्थापित:")
    print(dest)
