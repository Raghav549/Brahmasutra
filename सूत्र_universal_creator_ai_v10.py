# 🕉️ सूत्र Universal Creator AI v10
# Automatic APK Build + Install Command Generator

import os


class सूत्रUniversalCreatorAIv10:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/निर्माण")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण तंत्र तैयार")


    def नाम_प्राप्त(self, आदेश):

        words = आदेश.split()

        if len(words) >= 2:
            return words[1]

        return "सूत्रApp"


    def android_project_निर्माण(self, नाम):

        base = os.path.join(self.base, नाम+"_apk")

        java = os.path.join(base,"app/src/main/java/com/sutra")

        assets = os.path.join(base,"app/src/main/assets")

        os.makedirs(java, exist_ok=True)
        os.makedirs(assets, exist_ok=True)


        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{नाम}</title>
</head>
<body>

<h1>{नाम} App</h1>
<p>सूत्र Creator AI v10 द्वारा निर्मित</p>

</body>
</html>
"""

        with open(os.path.join(assets,"index.html"),"w",encoding="utf-8") as f:
            f.write(html)


        java_code = f"""
package com.sutra;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;

public class MainActivity extends Activity {{

    public void onCreate(Bundle b){{
        super.onCreate(b);

        WebView w = new WebView(this);

        w.loadUrl("file:///android_asset/index.html");

        setContentView(w);
    }}

}}
"""

        with open(os.path.join(java,"MainActivity.java"),"w",encoding="utf-8") as f:
            f.write(java_code)


        manifest = f"""
<manifest package="com.sutra.{नाम}"
xmlns:android="http://schemas.android.com/apk/res/android">

<application>

<activity android:name=".MainActivity">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>
"""

        manifest_path = os.path.join(base,"app/src/main/AndroidManifest.xml")

        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

        with open(manifest_path,"w",encoding="utf-8") as f:
            f.write(manifest)


        # Build script
        build_script = f"""#!/bin/bash

echo "Building APK..."

cd "{base}"

gradle assembleDebug

echo "APK build complete"

echo "Install command:"

echo "adb install app/build/outputs/apk/debug/app-debug.apk"
"""

        script_path = os.path.join(base,"build.sh")

        with open(script_path,"w",encoding="utf-8") as f:
            f.write(build_script)


        print("")
        print("APK Project निर्मित:", base)
        print("")
        print("Build script:", script_path)
        print("")
        print("Run:")
        print("bash", script_path)


    def निर्माण(self, आदेश):

        if आदेश.startswith("apk"):

            नाम = self.नाम_प्राप्त(आदेश)

            self.android_project_निर्माण(नाम)

        else:

            print("अज्ञात आदेश")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, आदेश

    print("🕉️ सूत्र Universal Creator AI v10 सक्रिय")


    # start

    ai = सूत्रUniversalCreatorAIv10()

    while True:

        आदेश = input("CreatorAIv10 >>> ")

        if आदेश == "निर्गम":
            break

        ai.निर्माण(आदेश)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
