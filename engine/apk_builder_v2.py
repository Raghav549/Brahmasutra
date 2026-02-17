import os
import shutil

OUTPUT_DIR = os.path.expanduser("~/सूत्र-तंत्र/apk_output")

def निर्माण(file):

    print("APK निर्माण प्रारंभ...")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    name = os.path.splitext(os.path.basename(file))[0]

    apk_path = os.path.join(OUTPUT_DIR, name + ".apk")

    with open(apk_path, "w") as f:
        f.write("SANSKRIT APK\n")
        f.write("APP NAME: " + name + "\n")

    print("APK सफलतया निर्मित:")
    print(apk_path)

    return apk_path


def स्थापित(apk):

    destination = "/sdcard/Download/" + os.path.basename(apk)

    shutil.copy(apk, destination)

    print("APK Download folder में स्थापित:")
    print(destination)
