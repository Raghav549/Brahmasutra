# 🕉️ ब्रह्म अनुप्रयोग निर्माता तंत्र
# VERSION 17


import os


class ब्रह्मअनुप्रयोगनिर्मातातंत्र:

    def __init__(self):

        self.app_dir = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_अनुप्रयोग")

        os.makedirs(self.app_dir, exist_ok=True)

        print("अनुप्रयोग निर्माता तैयार")


    # CREATE APP
    def निर्माण(self, नाम, कोड):

        file_path = os.path.join(self.app_dir, नाम + ".अनुप्रयोग")

        with open(file_path, "w", encoding="utf-8") as f:

            f.write(कोड)

        print("अनुप्रयोग निर्मित:", file_path)

        return file_path


    # CREATE DEFAULT APP
    def मूल_अनुप्रयोग(self, नाम):

        कोड = """

स्थापित अ 100
दर्शय अ

स्थापित ब 200
योग अ ब
दर्शय अ

"""

        return self.निर्माण(नाम, कोड)


    # LIST APPS
    def सूची(self):

        apps = os.listdir(self.app_dir)

        print("निर्मित अनुप्रयोग:")

        for app in apps:

            print("•", app)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global maker
    print("🕉️ ब्रह्म अनुप्रयोग निर्माता तंत्र सक्रिय")
    maker = ब्रह्मअनुप्रयोगनिर्मातातंत्र()

    maker.मूल_अनुप्रयोग("परीक्षण_ऐप")

    maker.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
