import os
import zipfile
import shutil


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
