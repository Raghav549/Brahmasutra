# 🕉️ सूत्र App Builder AI v1
# पूर्ण स्वदेशी अनुप्रयोग निर्माता कृत्रिमबुद्धि


import सूत्र_application_framework_v1 as framework


class सूत्रAppBuilderAI:


    def __init__(self):

        print("🕉️ सूत्र App Builder AI सक्रिय")

        self.framework = framework.सूत्रApplicationFramework()


    def प्रारम्भ(self):

        while True:

            print("")
            print("AI आदेश लिखें या 'निर्गम' लिखें")

            आदेश = input("AI >>> ")

            if आदेश == "निर्गम":

                break

            self.निर्माण(आदेश)


    def निर्माण(self, prompt):

        print("विश्लेषण:", prompt)

        app_name = self.extract_name(prompt)

        if app_name == None:

            print("अनुप्रयोग नाम नहीं मिला")

            return


        print("अनुप्रयोग निर्माण:", app_name)

        self.framework.register(app_name)

        print("अनुप्रयोग launch:", app_name)

        self.framework.start(app_name)


        self.generate_code(app_name)


    def extract_name(self, prompt):

        words = prompt.split()

        if len(words) >= 2:

            return words[-1]

        return None


    def generate_code(self, name):

        filename = name + ".सूत्र"

        print("Sanskrit code निर्माण:", filename)

        code = []

        code.append("संकल्प अ 10")

        code.append("संकल्प ब 20")

        code.append("योग अ ब")

        code.append("दर्शय अ")

        code.append("निर्गम")


        with open(filename,"w",encoding="utf-8") as f:

            for line in code:

                f.write(line + "\n")


        print("Sanskrit app code निर्मित:", filename)


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
