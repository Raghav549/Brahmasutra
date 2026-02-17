import os

print("🕉️ ब्रह्म AI अनुप्रयोग स्वनिर्माता VERSION 34 सक्रिय")

class ब्रह्मस्वनिर्माता:

    def निर्मित(self, prompt):

        name = prompt.replace(" ","_")

        base = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_AI_APPS/" + name

        os.makedirs(base, exist_ok=True)
        os.makedirs(base+"/frontend", exist_ok=True)
        os.makedirs(base+"/backend", exist_ok=True)
        os.makedirs(base+"/database", exist_ok=True)
        os.makedirs(base+"/api", exist_ok=True)

        self.frontend(base)
        self.backend(base)
        self.database(base)
        self.api(base)

        print("सफल अनुप्रयोग निर्मित:", base)

    def frontend(self, base):

        code = """<html>
<body>
<h1>BRAHMA GENERATED APP</h1>
<button onclick="test()">Test API</button>
<div id="out"></div>

<script>

function test(){

fetch("http://127.0.0.1:7000/test")
.then(r=>r.text())
.then(d=>{
document.getElementById("out").innerText=d
})

}

</script>

</body>
</html>
"""

        open(base+"/frontend/index.html","w").write(code)

    def backend(self, base):

        code = """from http.server import HTTPServer,BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path=="/test":

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()

            self.wfile.write(b"BRAHMA AI SUCCESS")

server=HTTPServer(("0.0.0.0",7000),H)

print("BACKEND RUNNING")

server.serve_forever()
"""

        open(base+"/backend/server.py","w").write(code)

    def database(self, base):

        open(base+"/database/db.txt","w").write("BRAHMA DATABASE")

    def api(self, base):

        open(base+"/api/api.txt","w").write("BRAHMA API")
