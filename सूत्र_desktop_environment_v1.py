# 🕉️ सूत्र Desktop Environment v1
# पूर्ण स्वदेशी desktop system


import सूत्र_window_manager_v1 as wm


class सूत्रDesktopEnvironment:

    def __init__(self):

        print("🕉️ सूत्र Desktop Environment निर्माण")

        self.window_manager = wm.सूत्रWindowManager()

        self.सक्रिय = True


    def प्रारम्भ(self):

        print("🕉️ सूत्र Desktop Environment सक्रिय")

        while self.सक्रिय:

            self.डेस्कटॉप()

            आदेश = input("Desktop >>> ")

            self.निष्पादन(आदेश)


    def डेस्कटॉप(self):

        print("")
        print("====== सूत्र Desktop ======")

        print("१. Window Manager खोलो")

        print("२. गणक खोलो")

        print("३. परीक्षण खोलो")

        print("४. OS स्थिति")

        print("५. निर्गम")

        print("===========================")


    def निष्पादन(self, आदेश):

        if आदेश == "१":

            self.window_manager.प्रारम्भ()


        elif आदेश == "२":

            print("गणक प्रारम्भ")

            self.window_manager.नई_खिड़की("गणक")


        elif आदेश == "३":

            print("परीक्षण प्रारम्भ")

            self.window_manager.नई_खिड़की("परीक्षण")


        elif आदेश == "४":

            self.window_manager.os.स्थिति()


        elif आदेश == "५":

            print("Desktop बन्द")

            self.window_manager.os.बन्द()

            self.सक्रिय = False


        else:

            print("अमान्य आदेश")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global desktop
    desktop = सूत्रDesktopEnvironment()

    desktop.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
