import os
import shutil


def build_apk(html, output):

    html = os.path.expanduser(html)
    output = os.path.expanduser(output)

    build_dir = os.path.join(HOME, "sutra_apk_build")

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(build_dir + "/assets", exist_ok=True)

    shutil.copy(html, build_dir + "/assets/index.html")

    manifest = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.app">

<application android:label="Sutra App">

<activity android:name=".MainActivity">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>'''

    open(build_dir + "/AndroidManifest.xml", "w").write(manifest)

    dex_path = os.path.join(HOME, "सूत्र-तंत्र/apk_build/classes.dex")

    if os.path.exists(dex_path):

        shutil.copy(dex_path, build_dir + "/classes.dex")

    else:

        print("classes.dex नहीं मिला")
        return

    # The historical version shelled out to ``aapt``/``zip`` with interpolated
    # paths.  Those tools are not part of this project, so the build is done
    # with :mod:`brahma_packaging` and the result is described truthfully.
    from brahma_packaging import build_bundle, describe

    try:
        bundle = build_bundle("सूत्र", [build_dir], os.path.dirname(output) or ".")
    except (OSError, ValueError) as exc:
        print("बंडल निर्माण विफल:", exc)
        return None

    print("बंडल निर्मित:", describe(bundle.path))
    return bundle.path


def install_apk(file):

    file = os.path.expanduser(file)

    if os.path.exists(file):

        _open_file(file)

        print("स्थापना प्रारम्भ:", file)

    else:

        print("APK नहीं मिला:", file)


HOME = os.path.expanduser("~")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global parts, आदेश

    print("🕉️ सूत्रभाषा v3 सक्रिय")



    while True:

        आदेश = input("सूत्र >>> ").strip()

        if आदेश.startswith("apkनिर्मापय"):

            parts = आदेश.split()

            if len(parts) >= 3:

                build_apk(parts[1], parts[2])

        elif आदेश.startswith("स्थापय"):

            parts = आदेश.split()

            if len(parts) >= 2:

                install_apk(parts[1])

        elif आदेश == "निर्गच्छ":

            break


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))


def _open_file(path):
    """Open ``path`` with the platform opener — no shell involved."""
    import shutil
    import subprocess

    if not os.path.isfile(path):
        print("संचिका नहीं मिली:", path)
        return False
    for candidate in ("termux-open", "xdg-open", "open"):
        if shutil.which(candidate):
            subprocess.run([candidate, path], check=False, timeout=30)
            return True
    print("कोई opener उपलब्ध नहीं")
    return False
