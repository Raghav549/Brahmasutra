# 🕉️ ब्रह्म अनुप्रयोग निष्पादन तंत्र
# VERSION 16


import os
import shutil

from ब्रह्म_कार्यक्रम_निष्पादन_कोर import ब्रह्मकार्यक्रमनिष्पादनकोर


class ब्रह्मअनुप्रयोगनिष्पादनतंत्र:

    def __init__(self):

        self.install_dir = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_स्थापित")

        os.makedirs(self.install_dir, exist_ok=True)

        self.executor = ब्रह्मकार्यक्रमनिष्पादनकोर()

        print("अनुप्रयोग तंत्र तैयार")


    # INSTALL APP
    def स्थापना(self, app_file):

        if not os.path.exists(app_file):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return


        name = os.path.basename(app_file)

        dest = os.path.join(self.install_dir, name)

        shutil.copy(app_file, dest)

        print("अनुप्रयोग स्थापित:", name)


    # LIST APPS
    def सूची(self):

        apps = os.listdir(self.install_dir)

        print("स्थापित अनुप्रयोग:")

        for app in apps:
            print("•", app)


    # RUN APP
    def निष्पादन(self, name):

        path = os.path.join(self.install_dir, name)

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")
            return


        print("अनुप्रयोग प्रारम्भ:", name)

        self.executor.कार्यक्रम_चलाओ(path)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म अनुप्रयोग निष्पादन तंत्र सक्रिय")
    system = ब्रह्मअनुप्रयोगनिष्पादनतंत्र()

    test_app = os.path.expanduser("~/सूत्र-तंत्र/test_app.अनुप्रयोग")

    with open(test_app, "w", encoding="utf-8") as f:

        f.write("""
स्थापित अ 999
दर्शय अ

स्थापित ब 100
योग अ ब
दर्शय अ
""")

    system.स्थापना(test_app)

    system.सूची()

    system.निष्पादन("test_app.अनुप्रयोग")


if __name__ == "__main__":
    _main()
