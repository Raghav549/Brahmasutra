import os
import random


class सूत्रएण्ड्रॉयडनिर्माता:


    def __init__(self):

        print("🕉️ सूत्र एण्ड्रॉयड अनुप्रयोग निर्माता सक्रिय")

        self.मूल_पथ = "निर्मित_एण्ड्रॉयड"

        if not os.path.exists(self.मूल_पथ):

            os.mkdir(self.मूल_पथ)


    def नाम_निर्माण(self):

        return "सूत्रएप्प" + str(random.randint(1000,9999))


    def संरचना_निर्माण(self, नाम):

        app_path = self.मूल_पथ + "/" + नाम

        os.makedirs(app_path + "/java", exist_ok=True)

        os.makedirs(app_path + "/res", exist_ok=True)

        os.makedirs(app_path + "/assets", exist_ok=True)


        self.manifest(नाम, app_path)

        self.main_activity(नाम, app_path)

        self.layout(नाम, app_path)


        print("एण्ड्रॉयड अनुप्रयोग संरचना निर्मित:", app_path)


    def manifest(self, नाम, path):

        content = f"""
<manifest package="{नाम}">
<application label="{नाम}">
<activity name="MainActivity"/>
</application>
</manifest>
"""

        with open(path + "/AndroidManifest.xml","w") as f:

            f.write(content)


    def main_activity(self, नाम, path):

        code = f"""
public class MainActivity {{

    public static void main(String[] args) {{

        System.out.println("🕉️ सूत्र एण्ड्रॉयड अनुप्रयोग सक्रिय");

    }}

}}
"""

        with open(path + "/java/MainActivity.java","w") as f:

            f.write(code)


    def layout(self, नाम, path):

        layout = f"""
<layout>
<text>सूत्र अनुप्रयोग: {नाम}</text>
</layout>
"""

        with open(path + "/res/layout.xml","w") as f:

            f.write(layout)


    def निर्माण(self):

        नाम = self.नाम_निर्माण()

        self.संरचना_निर्माण(नाम)
