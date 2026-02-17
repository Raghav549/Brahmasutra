# 🕉️ सूत्र Bootloader v2

import सूत्र_कर्ण_v2 as कर्ण
import सूत्र_shell_v3 as शेल


class सूत्रBootloaderV2:

    def __init__(self):

        print("🕉️ सूत्र Bootloader v2 सक्रिय")

        self.kernel = None
        self.shell = None


    def कर्ण_लोड(self):

        print("कर्ण लोड हो रहा है...")

        self.kernel = कर्ण

        print("कर्ण लोड सफल")


    def कर्ण_प्रारम्भ(self):

        print("कर्ण प्रारम्भ हो रहा है...")

        try:

            self.kernel.प्रारम्भ()

            print("कर्ण सक्रिय")

        except:

            print("कर्ण प्रारम्भ function नहीं मिला")


    def शेल_लोड(self):

        print("शेल लोड हो रहा है...")

        self.shell = शेल

        print("शेल लोड सफल")


    def शेल_प्रारम्भ(self):

        print("शेल प्रारम्भ हो रहा है...")

        try:

            self.shell.प्रारम्भ()

        except:

            print("शेल प्रारम्भ function नहीं मिला")


    def प्रारम्भ(self):

        print("🕉️ Bootloader v2 प्रारम्भ")

        self.कर्ण_लोड()

        self.कर्ण_प्रारम्भ()

        self.शेल_लोड()

        self.शेल_प्रारम्भ()

        print("🕉️ सूत्र OS पूर्ण सक्रिय")


# test

if __name__ == "__main__":

    boot = सूत्रBootloaderV2()

    boot.प्रारम्भ()
