import os
import shutil

BASE = os.path.expanduser("~/सूत्र-तंत्र")
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
