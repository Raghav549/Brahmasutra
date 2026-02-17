import time

class सूत्रBootloader:

    def __init__(self):

        self.स्थिति = "अप्रारम्भ"

    def प्रारम्भ(self):

        print("सूत्र Bootloader प्रारम्भ")

        self.स्थिति = "प्रारम्भ"

        self.प्रणाली_जाँच()

        self.kernel_प्रारम्भ()

        print("सूत्र OS सफलतया आरम्भित")

    def प्रणाली_जाँच(self):

        print("प्रणाली जाँच...")

        time.sleep(1)

        print("स्मृति जाँच सफल")

        print("CPU जाँच सफल")

        print("उपकरण जाँच सफल")

    def kernel_प्रारम्भ(self):

        print("Kernel लोड हो रहा है...")

        time.sleep(1)

        print("Kernel सफलतया लोड")
