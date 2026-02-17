# ब्रह्म GUI इंजन
# VERSION 112

import http.server
import socketserver
import json
import os

class ब्रह्मGUIइंजन:

    def __init__(self, पोर्ट=9090):
        self.पोर्ट = पोर्ट
        print("ब्रह्म GUI इंजन सक्रिय")

    def प्रारंभ(self):

        इंजन = self

        class GUIHandler(http.server.SimpleHTTPRequestHandler):

            def do_GET(self):

                if self.path == "/":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(इंजन.GUIपृष्ठ().encode())
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):

                if self.path == "/generate":

                    length = int(self.headers['Content-Length'])
                    data = self.rfile.read(length)
                    prompt = json.loads(data.decode())["prompt"]

                    response = {
                        "status": "success",
                        "message": "ब्रह्म ने prompt स्वीकार किया",
                        "prompt": prompt
                    }

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())


        with socketserver.TCPServer(("", self.पोर्ट), GUIHandler) as httpd:
            print(f"ब्रह्म GUI सर्वर प्रारंभ: http://127.0.0.1:{self.पोर्ट}")
            httpd.serve_forever()


    def GUIपृष्ठ(self):

        return """
<!DOCTYPE html>
<html>
<head>
<title>BRAHMA GUI ENGINE</title>
<style>

body {
background:#0b1220;
color:white;
font-family:Arial;
text-align:center;
padding-top:50px;
}

textarea{
width:80%;
height:150px;
font-size:16px;
}

button{
background:#00ff88;
border:none;
padding:15px 30px;
font-size:18px;
margin-top:20px;
cursor:pointer;
}

#result{
margin-top:30px;
color:#00ff88;
}

</style>
</head>

<body>

<h1>BRAHMA GUI ENGINE</h1>

<p>Prompt → App Generator</p>

<textarea id="prompt" placeholder="Enter your prompt here"></textarea>

<br>

<button onclick="generate()">Generate</button>

<div id="result"></div>

<script>

async function generate(){

let prompt = document.getElementById("prompt").value;

let res = await fetch("/generate",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({prompt:prompt})
});

let data = await res.json();

document.getElementById("result").innerText =
"Response: " + data.message;

}

</script>

</body>
</html>
"""


# standalone run

if __name__ == "__main__":
    gui = ब्रह्मGUIइंजन()
    gui.प्रारंभ()
