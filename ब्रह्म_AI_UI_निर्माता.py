# 🕉️ ब्रह्म AI UI निर्माता VERSION 23

import os

print("🕉️ ब्रह्म AI UI निर्माता VERSION 23 सक्रिय")


class ब्रह्मUINirmata:

    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_UI")

        os.makedirs(self.base, exist_ok=True)


    def निर्मित(self, name):

        app_path = os.path.join(self.base, name)

        os.makedirs(app_path, exist_ok=True)


        # LOGIN PAGE

        login = """

<html>

<head>
<title>ब्रह्म अनुप्रयोग</title>
</head>

<body>

<h1>लॉगिन</h1>

<input id="user" placeholder="नाम">

<input id="pass" placeholder="पासवर्ड" type="password">

<button onclick="login()">लॉगिन</button>

<script>

function login(){

alert("लॉगिन सफल")

}

</script>

</body>

</html>

"""

        with open(os.path.join(app_path,"login.html"),"w",encoding="utf-8") as f:
            f.write(login)



        # DASHBOARD

        dash = """

<html>

<head>
<title>डैशबोर्ड</title>
</head>

<body>

<h1>डैशबोर्ड</h1>

<button onclick="alert('AI सक्रिय')">

AI चलाओ

</button>

</body>

</html>

"""

        with open(os.path.join(app_path,"dashboard.html"),"w",encoding="utf-8") as f:
            f.write(dash)


        print("UI निर्मित:", app_path)

        return app_path



# run

engine = ब्रह्मUINirmata()

name = input("अनुप्रयोग नाम लिखें: ")

path = engine.निर्मित(name)

print("पूर्ण UI:", path)
