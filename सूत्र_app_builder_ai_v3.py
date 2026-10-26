# 🕉️ सूत्र App Builder AI v3
# पूर्ण स्वदेशी बहु-स्तरीय अनुप्रयोग निर्माता


import os

import सूत्र_application_framework_v1 as framework


class सूत्रAppBuilderAIv3:


    def __init__(self):

        print("🕉️ सूत्र App Builder AI v3 सक्रिय")

        self.framework = framework.सूत्रApplicationFramework()


        self.types = {

            "calculator":"calculator",
            "गणक":"calculator",

            "website":"website",
            "वेबसाइट":"website",

            "gui":"gui",
            "interface":"gui",

            "app":"app",
            "एप":"app"
        }


    def प्रारम्भ(self):

        while True:

            print("")
            आदेश = input("AIv3 >>> ")

            if आदेश == "निर्गम":

                break

            self.process(आदेश)


    def process(self, prompt):

        name = self.get_name(prompt)

        type = self.get_type(prompt)


        print("नाम:", name)

        print("प्रकार:", type)


        self.create_project(name, type)

        self.framework.register(name)

        self.framework.start(name)


    def get_name(self, prompt):

        words = prompt.split()

        if len(words) == 0:

            return "अनुप्रयोग"

        return words[-1]


    def get_type(self, prompt):

        words = prompt.lower().split()

        for w in words:

            if w in self.types:

                return self.types[w]

        return "app"


    def create_project(self, name, type):

        folder = name + "_project"

        if not os.path.exists(folder):

            os.mkdir(folder)


        if type == "website":

            self.create_website(folder, name)

        elif type == "calculator":

            self.create_calculator(folder, name)

        elif type == "gui":

            self.create_gui(folder, name)

        else:

            self.create_basic(folder, name)


    def create_website(self, folder, name):

        html = folder + "/index.html"

        content = f"""

<html>

<head>

<title>{name}</title>

</head>

<body>

<h1>🕉️ {name}</h1>

<p>सूत्र द्वारा निर्मित वेबसाइट</p>

</body>

</html>

"""

        with open(html,"w",encoding="utf-8") as f:

            f.write(content)

        print("Website निर्मित:", html)


    def create_calculator(self, folder, name):

        file = folder + "/" + name + ".सूत्र"

        code = [

            "संकल्प अ 100",

            "संकल्प ब 200",

            "योग अ ब",

            "दर्शय अ",

            "निर्गम"

        ]

        with open(file,"w",encoding="utf-8") as f:

            for line in code:

                f.write(line + "\n")

        print("Calculator निर्मित:", file)


    def create_gui(self, folder, name):

        file = folder + "/interface.txt"

        content = "सूत्र GUI अनुप्रयोग"

        with open(file,"w",encoding="utf-8") as f:

            f.write(content)

        print("GUI निर्मित:", file)


    def create_basic(self, folder, name):

        file = folder + "/main.सूत्र"

        code = [

            "संकल्प मान 999",

            "दर्शय मान",

            "निर्गम"

        ]

        with open(file,"w",encoding="utf-8") as f:

            for line in code:

                f.write(line + "\n")

        print("Basic app निर्मित:", file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai
    ai = सूत्रAppBuilderAIv3()

    ai.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
