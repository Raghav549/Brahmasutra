import os
import shutil

print("🕉️ सूत्रभाषा v3 सक्रिय")

HOME = os.path.expanduser("~")


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

    os.system(f"""
    cd {build_dir} &&
    aapt package -f -M AndroidManifest.xml -A assets -F sutra.apk &&
    zip -u sutra.apk classes.dex &&
    cp sutra.apk {output}
    """)

    print("APK निर्मित:", output)


def install_apk(file):

    file = os.path.expanduser(file)

    if os.path.exists(file):

        os.system(f"termux-open '{file}'")

        print("स्थापना प्रारम्भ:", file)

    else:

        print("APK नहीं मिला:", file)


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
