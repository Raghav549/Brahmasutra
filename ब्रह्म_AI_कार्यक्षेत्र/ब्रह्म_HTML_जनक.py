# ब्रह्म HTML जनक
# VERSION 124 SUPPORT FILE

import os


class ब्रह्मHTMLजनक:

    def __init__(self, frontend_dir):

        self.frontend_dir = frontend_dir

        print("ब्रह्म HTML जनक सक्रिय")


    def जनन(self, app_name):

        html_path = os.path.join(self.frontend_dir, "index.html")


        html_code = f"""
<!DOCTYPE html>
<html>
<head>
<title>{app_name}</title>
<style>

body {{
font-family: Arial;
background: #0f172a;
color: white;
text-align: center;
margin-top: 100px;
}}

button {{
padding: 15px;
font-size: 18px;
background: #2563eb;
color: white;
border: none;
border-radius: 10px;
cursor: pointer;
}}

</style>
</head>

<body>

<h1>Brahma Generated App</h1>

<p>{app_name} ready</p>

<button onclick="callBackend()">Test Backend</button>

<p id="output"></p>

<script>

function callBackend() {{

fetch("http://127.0.0.1:5000/")
.then(r=>r.json())
.then(d=>{{
document.getElementById("output").innerText =
JSON.stringify(d)
}})
.catch(e=>{{
document.getElementById("output").innerText =
"Backend error"
}})

}}

</script>

</body>
</html>
"""


        with open(html_path, "w", encoding="utf-8") as f:

            f.write(html_code)


        print("Frontend generated:", html_path)
