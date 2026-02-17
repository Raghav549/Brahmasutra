print("🕉️ ब्रह्म सिस्टम प्रारम्भ")


from ब्रह्म_बूट_लोडर import ब्रह्मबूटलोडर


class ब्रह्मसिस्टम:


    def __init__(self):

        print("BRAHMA SYSTEM POWER ON")

        self.bootloader = ब्रह्मबूटलोडर()


    def प्रारम्भ(self):

        print("SYSTEM START")

        filename = input("Enter binary filename: ")

        self.bootloader.बूट(filename)
