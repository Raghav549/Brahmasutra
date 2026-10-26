# 🕉️ BRAHMA AI VERSION 9
# Full Application Linker Engine

import os

class ब्रह्मAILinker:

    def __init__(self):

        print("🕉️ ब्रह्म AI लिंकर VERSION 9 सक्रिय")

        self.root = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")


    def लिंक(self, app_name):

        app_path = os.path.join(self.root, app_name)

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return


        files = os.listdir(app_path)

        main_file = os.path.join(app_path, "मुख्य.ब्रह्म")


        with open(main_file, "w", encoding="utf-8") as main:

            main.write("दर्शय अनुप्रयोग_प्रारम्भ\n")


            for file in files:

                if file != "मुख्य.ब्रह्म":

                    module_name = file.replace(".ब्रह्म", "")

                    main.write("दर्शय " + module_name + "\n")


            main.write("दर्शय अनुप्रयोग_समाप्त\n")


        print("पूर्ण अनुप्रयोग लिंक सफल")

        print(main_file)

        return main_file


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global linker, name
    linker = ब्रह्मAILinker()

    name = input("अनुप्रयोग नाम: ")

    linker.लिंक(name)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
