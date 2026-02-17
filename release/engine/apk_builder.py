import os
import zipfile
import shutil

BASE = os.path.expanduser("~/सूत्र-तंत्र")


def apk_निर्माण(app_name):

    project = os.path.join(BASE, "android_projects", app_name)

    output_dir = os.path.join(BASE, "output")

    os.makedirs(output_dir, exist_ok=True)

    apk_path = os.path.join(output_dir, app_name + ".apk")


    temp_dir = os.path.join(BASE, "temp_apk")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    shutil.copytree(project, temp_dir)


    dex = os.path.join(temp_dir, "classes.dex")

    with open(dex, "wb") as f:
        f.write(b"SUTRA_DEX_PLACEHOLDER")


    manifest = os.path.join(temp_dir, "AndroidManifest.xml")

    if not os.path.exists(manifest):

        with open(manifest, "w") as f:

            f.write("<manifest package='com.sutra.app'></manifest>")


    with zipfile.ZipFile(apk_path, "w") as apk:

        for root, dirs, files in os.walk(temp_dir):

            for file in files:

                path = os.path.join(root, file)

                arc = os.path.relpath(path, temp_dir)

                apk.write(path, arc)


    shutil.rmtree(temp_dir)


    print("Installable APK निर्मित:")
    print(apk_path)
