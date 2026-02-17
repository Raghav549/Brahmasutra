import os
import subprocess
import random

print("🕉️ सूत्र Universal Creator AI v20 सक्रिय")

class सूत्रCreatorAIv20:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v20")
        os.makedirs(self.base, exist_ok=True)

        print("निर्माण पथ:", self.base)


    def नाम_निकालो(self, prompt):

        words = prompt.split()

        if len(words) >= 2:
            return words[1]

        return "app_" + str(random.randint(1000,9999))


    def apk_निर्माण(self, name):

        path = os.path.join(self.base, name)
        os.makedirs(path, exist_ok=True)

        apk = os.path.join(path, name + ".apk")

        with open(apk,"wb") as f:
            f.write(b"SUTRA_APK_" + name.encode())

        print("APK निर्मित:", apk)

        return apk


    def install(self, apk):

        print("Install प्रारम्भ")

        try:
            subprocess.run(["termux-open", apk])
            print("Install screen launched")

        except:
            print("Install failed")


    def launch(self, name):

        print("Launch simulation:", name)
        print(name, "App launched")


    def create(self, prompt):

        name = self.नाम_निकालो(prompt)

        print("नाम:", name)

        apk = self.apk_निर्माण(name)

        self.install(apk)

        self.launch(name)


ai = सूत्रCreatorAIv20()

while True:

    cmd = input("CreatorAIv20 >>> ")

    if cmd == "निर्गम":
        break

    if cmd.startswith("create") or cmd.startswith("app"):

        ai.create(cmd)

    else:

        print("अज्ञात आदेश")
