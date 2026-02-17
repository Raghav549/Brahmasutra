# 🕉️ सूत्र Universal Creator AI v7

import os
import http.server
import socketserver

print("🕉️ सूत्र Universal Creator AI v7 सक्रिय")


class सूत्रUniversalCreatorAIv7:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/निर्माण")

        os.makedirs(self.base, exist_ok=True)

        print("निर्माण तंत्र तैयार")


    # नाम निकालना
    def नाम_प्राप्त(self, आदेश):

        words = आदेश.split()

        if len(words) >= 2:
            return words[1]

        return "सूत्र_निर्माण"


    # Website निर्माण
    def website_निर्माण(self, नाम):

        folder = os.path.join(self.base, नाम+"_website")

        os.makedirs(folder, exist_ok=True)

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{नाम}</title>
</head>

<body>

<h1>{नाम} Website</h1>

<p>सूत्र Universal Creator AI v7 द्वारा निर्मित</p>

</body>
</html>
"""

        path = os.path.join(folder,"index.html")

        with open(path,"w",encoding="utf-8") as f:
            f.write(html)

        print("Website निर्मित:", folder)

        return folder


    # App निर्माण (basic structure)
    def app_निर्माण(self, नाम):

        folder = os.path.join(self.base, नाम+"_app")

        os.makedirs(folder, exist_ok=True)

        main = f"""
print("🕉️ {नाम} App सक्रिय")
"""

        path = os.path.join(folder,"main.py")

        with open(path,"w",encoding="utf-8") as f:
            f.write(main)

        print("App निर्मित:", folder)


    # Server run
    def server_चलाओ(self, folder):

        os.chdir(folder)

        PORT = 8080

        handler = http.server.SimpleHTTPRequestHandler

        print("Server चल रहा है: http://localhost:8080")

        with socketserver.TCPServer(("", PORT), handler) as httpd:
            httpd.serve_forever()


    # Command process
    def निर्माण(self, आदेश):

        if आदेश.startswith("website"):

            नाम = self.नाम_प्राप्त(आदेश)

            folder = self.website_निर्माण(नाम)

            self.server_चलाओ(folder)


        elif आदेश.startswith("app"):

            नाम = self.नाम_प्राप्त(आदेश)

            self.app_निर्माण(नाम)


        else:

            print("अज्ञात आदेश")


# AI start

ai = सूत्रUniversalCreatorAIv7()

while True:

    आदेश = input("CreatorAIv7 >>> ")

    if आदेश == "निर्गम":
        break

    ai.निर्माण(आदेश)
