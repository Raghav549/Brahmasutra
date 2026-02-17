import os

class सूत्रAPKनिर्माता:

    def __init__(self):

        self.मूल = os.path.expanduser("~/सूत्र-तंत्र/apk")

        self.परियोजना = os.path.join(self.मूल, "सूत्रApp")

        self.java = os.path.join(self.परियोजना, "MainActivity.java")

        self.manifest = os.path.join(self.परियोजना, "AndroidManifest.xml")


    def निर्माण(self):

        print("सूत्र APK परियोजना निर्माण प्रारम्भ")


        os.makedirs(self.परियोजना, exist_ok=True)


        with open(self.manifest, "w", encoding="utf-8") as f:

            f.write("""<manifest package="org.sutra.app">

<application>

<activity android:name=".MainActivity">

<intent-filter>

<action android:name="android.intent.action.MAIN"/>

<category android:name="android.intent.category.LAUNCHER"/>

</intent-filter>

</activity>

</application>

</manifest>""")


        with open(self.java, "w", encoding="utf-8") as f:

            f.write("""public class MainActivity {

public static void main(String[] args){

System.out.println("सूत्र OS सक्रिय");

}

}""")


        print("परियोजना सफलतया निर्मिता")

        print("स्थान:", self.परियोजना)
