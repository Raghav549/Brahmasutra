# 🕉️ सूत्र GUI v1
# पूर्ण स्वदेशी graphical interface


import सूत्र_os_v3 as os_v3


class सूत्रGUIv1:

    def __init__(self):

        print("🕉️ सूत्र GUI निर्माण")

        self.os = os_v3.सूत्रOSv3()

        self.os.बूट()

        self.सक्रिय = True

        self.खिड़कियाँ = []


    def प्रारम्भ(self):

        print("🕉️ सूत्र GUI सक्रिय")

        while self.सक्रिय:

            self.डेस्कटॉप()

            आदेश = input("GUI >>> ")

            self.निष्पादन(आदेश)


    def डेस्कटॉप(self):

        print("")
        print("====== सूत्र Desktop ======")

        print("अनुप्रयोग:")

        print("१. गणक")
        print("२. परीक्षण")
        print("३. स्थिति")
        print("४. निर्गम")

        print("===========================")


    def निष्पादन(self, आदेश):

        if आदेश == "१":

            self.अनुप्रयोग_चलाओ("गणक")


        elif आदेश == "२":

            self.अनुप्रयोग_चलाओ("परीक्षण")


        elif आदेश == "३":

            self.os.स्थिति()


        elif आदेश == "४":

            print("GUI बन्द")

            self.os.बन्द()

            self.सक्रिय = False


        else:

            print("अमान्य चयन")


    def अनुप्रयोग_चलाओ(self, नाम):

        print("अनुप्रयोग प्रारम्भ:", नाम)

        self.खिड़कियाँ.append(नाम)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global gui
    gui = सूत्रGUIv1()

    gui.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
