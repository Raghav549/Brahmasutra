import os
import zipfile

def apk_निर्माण(project_name):

    print("APK निर्माण आरम्भ:")

    base_dir = os.path.expanduser("~/सूत्र-तंत्र")

    build_dir = os.path.join(base_dir, "apk_build")

    output_dir = os.path.join(base_dir, "apk_output")


    if not os.path.exists(build_dir):

        os.makedirs(build_dir)


    if not os.path.exists(output_dir):

        os.makedirs(output_dir)


    apk_path = os.path.join(output_dir, project_name + ".apk")


    # basic android structure

    manifest = '''<manifest package="com.sutra.app"
xmlns:android="http://schemas.android.com/apk/res/android">
<application android:label="सूत्र अनुप्रयोग">
</application>
</manifest>
'''


    manifest_path = os.path.join(build_dir, "AndroidManifest.xml")

    with open(manifest_path, "w", encoding="utf-8") as f:

        f.write(manifest)


    # create dummy classes.dex

    dex_path = os.path.join(build_dir, "classes.dex")

    with open(dex_path, "wb") as f:

        f.write(b"sutra-dex")


    # zip to apk

    with zipfile.ZipFile(apk_path, "w") as apk:

        apk.write(manifest_path, "AndroidManifest.xml")

        apk.write(dex_path, "classes.dex")


    print("APK सफलतापूर्वक निर्मित:")
    print(apk_path)
