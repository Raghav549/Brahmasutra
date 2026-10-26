# ब्रह्म AI FRONTEND GENERATOR

import os



class ब्रह्मफ्रंटेंड:


    def निर्मित(self,नाम):

        path = f"{BASE}/{नाम}"

        os.makedirs(path, exist_ok=True)


        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{नाम}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>

body {{
font-family: Arial;
background: #0f172a;
color: white;
text-align: center;
padding: 50px;
}}

button {{
padding: 15px;
margin: 10px;
background: #22c55e;
border: none;
color: white;
font-size: 18px;
}}

</style>
</head>

<body>

<h1>{नाम} — BRAHMA AI APP</h1>

<button onclick="login()">Login</button>
<button onclick="dashboard()">Dashboard</button>

<script>

function login() {{
alert("Login System Ready")
}}

function dashboard() {{
alert("Dashboard Ready")
}}

</script>

</body>
</html>
"""


        with open(path+"/index.html","w",encoding="utf-8") as f:

            f.write(html)


        print("Frontend निर्मित:",path)

        return path


BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_FRONTEND")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global f

    print("🕉️ ब्रह्म AI Frontend Generator सक्रिय")



    os.makedirs(BASE, exist_ok=True)
    f = ब्रह्मफ्रंटेंड()

    f.निर्मित("test_app")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
