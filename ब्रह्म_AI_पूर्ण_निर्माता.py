# 🕉️ ब्रह्म AI पूर्ण अनुप्रयोग निर्माता VERSION 44

import os

from ब्रह्म_AI_विश्लेषक import ब्रह्मविश्लेषक
from ब्रह्म_AI_बैकएंड_निर्माता import ब्रह्मबैकएंडनिर्माता
from ब्रह्म_AI_फ्रंटएंड_निर्माता import ब्रह्मफ्रंटएंडनिर्माता
from ब्रह्म_AI_डेटाबेस_निर्माता import ब्रह्मडेटाबेसनिर्माता


class ब्रह्मपूर्णनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म पूर्ण निर्माता सक्रिय")

        self.विश्लेषक = ब्रह्मविश्लेषक()

        self.backend = ब्रह्मबैकएंडनिर्माता()

        self.frontend = ब्रह्मफ्रंटएंडनिर्माता()

        self.database = ब्रह्मडेटाबेसनिर्माता()


    def निर्माण(self, prompt):

        print("Prompt विश्लेषण...")

        app_name = prompt.replace(" ", "_")

        print("App:", app_name)

        print("Backend निर्माण...")

        self.backend.निर्माण(app_name)

        print("Frontend निर्माण...")

        self.frontend.निर्माण(app_name)

        print("Database निर्माण...")

        self.database.डेटाबेस_निर्माण(app_name)

        print("🕉️ पूर्ण अनुप्रयोग निर्मित:", app_name)

        return app_name


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global brahma, prompt
    brahma = ब्रह्मपूर्णनिर्माता()

    prompt = input("Prompt लिखें: ")

    brahma.निर्माण(prompt)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
