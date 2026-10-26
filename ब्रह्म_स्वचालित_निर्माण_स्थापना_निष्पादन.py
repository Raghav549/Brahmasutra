# 🕉️ ब्रह्म स्वचालित निर्माण स्थापना निष्पादन तंत्र

from ब्रह्म_प्रॉम्प्ट_अनुप्रयोग_निर्माता import ब्रह्मप्रॉम्प्टअनुप्रयोगनिर्माता
from ब्रह्म_अनुप्रयोग_स्थापक import ब्रह्मस्थापक


class ब्रह्मस्वचालिततंत्र:

    def __init__(self):

        print("🕉️ ब्रह्म स्वचालित निर्माण स्थापना निष्पादन तंत्र सक्रिय")

        self.creator = ब्रह्मप्रॉम्प्टअनुप्रयोगनिर्माता()

        self.installer = ब्रह्मस्थापक()


    def चलाओ(self, prompt):

        print("Prompt प्राप्त:", prompt)

        # create
        path = self.creator.निर्माण(prompt)

        # install
        self.installer.स्थापना(path)

        # extract name
        name = path.split("/")[-1]

        # execute
        print("अनुप्रयोग निष्पादन प्रारम्भ")

        self.installer.निष्पादन(name)

        print("पूर्ण स्वचालित निष्पादन पूर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global prompt, system
    system = ब्रह्मस्वचालिततंत्र()

    prompt = input("Prompt लिखें: ")

    system.चलाओ(prompt)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
