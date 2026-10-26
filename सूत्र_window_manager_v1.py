# 🕉️ सूत्र Window Manager v1
# पूर्ण स्वदेशी window नियंत्रण प्रणाली


import सूत्र_os_v3 as os_v3


class सूत्रखिड़की:

    def __init__(self, नाम):

        self.नाम = नाम

        self.स्थिति = "सक्रिय"

        print("खिड़की निर्मित:", नाम)


    def बन्द(self):

        self.स्थिति = "बन्द"

        print("खिड़की बन्द:", self.नाम)



class सूत्रWindowManager:

    def __init__(self):

        print("🕉️ सूत्र Window Manager निर्माण")

        self.os = os_v3.सूत्रOSv3()

        self.os.बूट()

        self.खिड़कीसूची = []

        self.सक्रिय = True


    def प्रारम्भ(self):

        print("🕉️ Window Manager सक्रिय")

        while self.सक्रिय:

            self.डेस्कटॉप()

            आदेश = input("WM >>> ")

            self.निष्पादन(आदेश)


    def डेस्कटॉप(self):

        print("")
        print("====== सूत्र Desktop ======")

        print("१. नई खिड़की")

        print("२. खिड़की सूची")

        print("३. खिड़की बन्द")

        print("४. OS स्थिति")

        print("५. निर्गम")

        print("===========================")


    def निष्पादन(self, आदेश):

        if आदेश == "१":

            नाम = input("खिड़की नाम: ")

            self.नई_खिड़की(नाम)


        elif आदेश == "२":

            self.सूची()


        elif आदेश == "३":

            नाम = input("खिड़की नाम: ")

            self.बन्द(नाम)


        elif आदेश == "४":

            self.os.स्थिति()


        elif आदेश == "५":

            print("Window Manager बन्द")

            self.os.बन्द()

            self.सक्रिय = False


        else:

            print("अमान्य आदेश")


    def नई_खिड़की(self, नाम):

        खिड़की = सूत्रखिड़की(नाम)

        self.खिड़कीसूची.append(खिड़की)


    def सूची(self):

        print("खिड़कियाँ:")

        for k in self.खिड़कीसूची:

            print(k.नाम, "-", k.स्थिति)


    def बन्द(self, नाम):

        for k in self.खिड़कीसूची:

            if k.नाम == नाम:

                k.बन्द()

                return

        print("खिड़की नहीं मिली")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global wm
    wm = सूत्रWindowManager()

    wm.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
