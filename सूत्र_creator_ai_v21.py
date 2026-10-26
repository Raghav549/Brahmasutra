import os
import random
import subprocess

class सूत्रCreatorAIv21:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/सर्वनिर्माण_v21")
        os.makedirs(self.base, exist_ok=True)

        print("निर्माण पथ:", self.base)


    def नाम_निकालो(self, prompt):

        words = prompt.split()

        if len(words) >= 2:
            return words[1]

        return "app_" + str(random.randint(1000,9999))


    def संरचना_निर्माण(self, name):

        root = os.path.join(self.base, name)

        folders = [
            "apk",
            "website",
            "game",
            "code",
            "assets"
        ]

        for f in folders:
            os.makedirs(os.path.join(root,f), exist_ok=True)

        return root


    def website_निर्माण(self, root, name):

        html = os.path.join(root,"website","index.html")

        content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name}</title>
</head>
<body>
<h1>🕉️ {name} Website</h1>
<p>सूत्र Creator AI v21 द्वारा निर्मित</p>
</body>
</html>
"""

        with open(html,"w",encoding="utf-8") as f:
            f.write(content)

        print("Website निर्मित")


    def apk_निर्माण(self, root, name):

        apk = os.path.join(root,"apk",name+".apk")

        with open(apk,"wb") as f:
            f.write(b"SUTRA_REAL_APK_"+name.encode())

        print("APK निर्मित")

        return apk


    def game_निर्माण(self, root, name):

        game = os.path.join(root,"game","main.py")

        code = f"""
print("🕉️ {name} Game प्रारम्भ")
print("Game running")
"""

        with open(game,"w",encoding="utf-8") as f:
            f.write(code)

        print("Game निर्मित")


    def launch(self, root):

        website = os.path.join(root,"website","index.html")

        subprocess.run(["termux-open", website])

        print("Website launched")


    def create(self, prompt):

        name = self.नाम_निकालो(prompt)

        print("नाम:", name)

        root = self.संरचना_निर्माण(name)

        self.website_निर्माण(root,name)

        self.game_निर्माण(root,name)

        apk = self.apk_निर्माण(root,name)

        self.launch(root)

        print("पूर्ण निर्माण:", root)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, cmd

    print("🕉️ सूत्र Universal Creator AI v21 सक्रिय")


    ai = सूत्रCreatorAIv21()

    while True:

        cmd = input("CreatorAIv21 >>> ")

        if cmd == "निर्गम":
            break

        if cmd.startswith("create") or cmd.startswith("app") or cmd.startswith("website"):

            ai.create(cmd)

        else:

            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
