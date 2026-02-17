# ब्रह्म_फ्रंटएंड_जनक.py
# BRAHMA FRONTEND GENERATOR
# VERSION 130

import os


class ब्रह्मफ्रंटएंडजनक:

    def __init__(self, base_path):

        self.base_path = base_path

        print("ब्रह्म फ्रंटएंड जनक सक्रिय")


    def निर्माण(self, app_name, architecture):

        frontend_path = os.path.join(
            self.base_path,
            app_name,
            "frontend"
        )

        os.makedirs(frontend_path, exist_ok=True)


        html_code = '''
<!DOCTYPE html>
<html>

<head>

<title>Brahma App</title>

<style>

body{

font-family:Arial;
background:#0f172a;
color:white;
text-align:center;
padding:50px;

}

button{

padding:15px;
margin:10px;
background:#22c55e;
border:none;
color:white;
cursor:pointer;
font-size:16px;

}

.card{

background:#1e293b;
padding:20px;
margin:20px;

}

</style>

</head>

<body>


<h1>BRAHMA GENERATED APP</h1>


<div class="card">

<button onclick="health()">Check Backend</button>

<button onclick="login()">Login</button>

<button onclick="dashboard()">Dashboard</button>

</div>


<pre id="output"></pre>


<script>

function health(){

fetch("http://127.0.0.1:7000/health")

.then(r=>r.json())

.then(d=>{

document.getElementById("output").innerText=

JSON.stringify(d,null,2)

})

}


function login(){

fetch("http://127.0.0.1:7000/login",{

method:"POST"

})

.then(r=>r.json())

.then(d=>{

document.getElementById("output").innerText=

JSON.stringify(d,null,2)

})

}


function dashboard(){

fetch("http://127.0.0.1:7000/dashboard")

.then(r=>r.json())

.then(d=>{

document.getElementById("output").innerText=

JSON.stringify(d,null,2)

})

}


</script>


</body>

</html>
'''


        html_file = os.path.join(
            frontend_path,
            "index.html"
        )


        with open(
            html_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html_code)


        print("फ्रंटएंड निर्मित:", frontend_path)

        return frontend_path
