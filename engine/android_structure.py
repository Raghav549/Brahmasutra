import os

def संरचना_निर्माण(app_name):

    base = os.path.expanduser("~/सूत्र-तंत्र")

    project = os.path.join(base, "android_projects", app_name)


    dirs = [

        "src",

        "res",

        "res/layout",

        "res/values",

        "assets",

        "META-INF"

    ]


    for d in dirs:

        os.makedirs(os.path.join(project, d), exist_ok=True)


    manifest = f'''
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.sutra.{app_name}">

<application
android:label="{app_name}"
android:allowBackup="true">

</application>

</manifest>
'''


    with open(os.path.join(project, "AndroidManifest.xml"), "w", encoding="utf-8") as f:

        f.write(manifest)


    print("Android संरचना निर्मित:")
    print(project)
