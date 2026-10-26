# 🕉️ सूत्र App Builder AI v2
# पूर्ण स्वदेशी बहुभाषी अनुप्रयोग निर्माता कृत्रिमबुद्धि


import सूत्र_application_framework_v1 as framework


class सूत्रAppBuilderAI:


    def __init__(self):

        print("🕉️ सूत्र App Builder AI v2 सक्रिय")

        self.framework = framework.सूत्रApplicationFramework()


        self.known_types = {

            "गणक":"calculator",
            "calculator":"calculator",
            "calc":"calculator",

            "खेल":"game",
            "game":"game",

            "वेबसाइट":"website",
            "website":"website",

            "एप":"app",
            "app":"app"
        }


    def प्रारम्भ(self):

        while True:

            print("")
            print("AI आदेश लिखें या 'निर्गम' लिखें")

            आदेश = input("AI >>> ")

            if आदेश == "निर्गम":

                break

            self.process_prompt(आदेश)


    def process_prompt(self, prompt):

        print("विश्लेषण प्रारम्भ...")

        app_name = self.extract_name(prompt)

        app_type = self.detect_type(prompt)


        print("अनुप्रयोग नाम:", app_name)

        print("अनुप्रयोग प्रकार:", app_type)


        self.build(app_name, app_type)


    def extract_name(self, prompt):

        words = prompt.split()

        if len(words) == 0:

            return "अनुप्रयोग"


        last = words[-1]

        return last


    def detect_type(self, prompt):

        words = prompt.lower().split()

        for w in words:

            if w in self.known_types:

                return self.known_types[w]

        return "app"


    def build(self, name, type):

        print("निर्माण प्रारम्भ:", name)

        self.framework.register(name)

        self.framework.start(name)

        self.generate_code(name, type)


    def generate_code(self, name, type):

        filename = name + ".सूत्र"

        print("Sanskrit code निर्माण:", filename)


        code = []


        if type == "calculator":

            code = [

                "संकल्प अ 50",

                "संकल्प ब 70",

                "योग अ ब",

                "दर्शय अ",

                "निर्गम"

            ]


        elif type == "game":

            code = [

                "संकल्प अंक 10",

                "दर्शय अंक",

                "निर्गम"

            ]


        else:

            code = [

                "संकल्प मान 100",

                "दर्शय मान",

                "निर्गम"

            ]


        with open(filename,"w",encoding="utf-8") as f:

            for line in code:

                f.write(line + "\n")


        print("अनुप्रयोग पूर्ण निर्मित:", filename)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai
    ai = सूत्रAppBuilderAI()

    ai.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
