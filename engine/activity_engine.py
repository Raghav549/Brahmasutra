import os

def गतिविधि_निर्माण(app_name):

    base = os.path.expanduser("~/सूत्र-तंत्र/build/" + app_name)

    java_path = base + "/app/src/main/java/org/sutra/app/MainActivity.java"

    xml_path = base + "/app/src/main/res/layout/activity_main.xml"

    values_path = base + "/app/src/main/res/values/strings.xml"


    java_code = f"""
package org.sutra.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{

        super.onCreate(savedInstanceState);

        TextView tv = new TextView(this);

        tv.setText("नमस्ते — सूत्र अनुप्रयोगः");

        setContentView(tv);
    }}
}}
"""

    os.makedirs(os.path.dirname(java_path), exist_ok=True)

    with open(java_path,"w",encoding="utf-8") as f:

        f.write(java_code)


    xml_code = """
<LinearLayout
xmlns:android="http://schemas.android.com/apk/res/android"
android:layout_width="match_parent"
android:layout_height="match_parent"
android:orientation="vertical">
</LinearLayout>
"""

    os.makedirs(os.path.dirname(xml_path), exist_ok=True)

    with open(xml_path,"w",encoding="utf-8") as f:

        f.write(xml_code)


    strings = f"""
<resources>

<string name="app_name">{app_name}</string>

</resources>
"""

    os.makedirs(os.path.dirname(values_path), exist_ok=True)

    with open(values_path,"w",encoding="utf-8") as f:

        f.write(strings)


    print("गतिविधि निर्मिता:")
    print(app_name)
