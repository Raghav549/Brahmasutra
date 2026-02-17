# 🕉️ सूत्र Universal Creator AI v9
# REAL Android APK Project Generator

import os

print("🕉️ सूत्र Universal Creator AI v9 सक्रिय")


class सूत्रUniversalCreatorAIv9:

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


        # HTML UI
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{नाम}</title>
</head>
<body>

<h1>{नाम} App</h1>
<p>सूत्र Creator AI v9 द्वारा निर्मित</p>

</body>
</html>
"""

        with open(os.path.join(assets,"index.html"),"w",encoding="utf-8") as f:
            f.write(html)


        # Java Wrapper
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


        # Manifest
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


        print("APK Project निर्मित:", base)

        print("")
        print("Build command:")
        print("")
        print("cd", base)
        print("gradle assembleDebug")


    def निर्माण(self, आदेश):

        if आदेश.startswith("apk"):

            नाम = self.नाम_प्राप्त(आदेश)

            self.android_project_निर्माण(नाम)

        else:

            print("अज्ञात आदेश")


# start

ai = सूत्रUniversalCreatorAIv9()

while True:

    आदेश = input("CreatorAIv9 >>> ")

    if आदेश == "निर्गम":
        break

    ai.निर्माण(आदेश)
