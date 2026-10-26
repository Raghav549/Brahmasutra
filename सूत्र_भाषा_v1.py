# 🕉️ सूत्र भाषा v1 — संचिका समर्थन सहित


import सूत्र_व्याख्याकार as व्याख्या


class सूत्रभाषा:


    def __init__(self):

        print("🕉️ सूत्र भाषा v1 सक्रिय")

        self.व्याख्याकार = व्याख्या.व्याख्याकार()


    def संचिका_चलाओ(self, नाम):

        try:

            self.व्याख्याकार.संचिका_चलाओ(नाम)

        except FileNotFoundError:

            print("संचिका नहीं मिली:", नाम)


    def संवाद(self):

        print("सूत्र संवाद प्रारम्भ")
        print("निर्गम लिखकर बन्द करें")

        while True:

            आदेश = input("सूत्र >>> ").strip()


            if आदेश == "निर्गम":

                print("सूत्र भाषा बन्द")
                break


            भाग = आदेश.split()


            if len(भाग) > 0 and भाग[0] == "संचिका":

                if len(भाग) > 1:

                    self.संचिका_चलाओ(भाग[1])

                else:

                    print("संचिका नाम आवश्यक है")

            else:

                self.व्याख्याकार.विश्लेषक.चलाओ(आदेश)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global भाषा
    भाषा = सूत्रभाषा()

    भाषा.संवाद()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
