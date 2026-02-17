# 🕉️ BRAHMA VERSION 2
# सूत्र शब्द प्रणाली

from सूत्र_वर्ण import वर्णप्रणाली

print("🕉️ सूत्र शब्द प्रणाली सक्रिय")

class शब्दप्रणाली:

    def __init__(self):

        self.वर्ण = वर्णप्रणाली()

    def मान्य(self, शब्द):

        if len(शब्द) == 0:

            return False

        for अक्षर in शब्द:

            if not self.वर्ण.मान्य(अक्षर):

                return False

        return True


# परीक्षण
if __name__ == "__main__":

    प्रणाली = शब्दप्रणाली()

    परीक्षण_सूची = [
        "अ",
        "कर्म",
        "फल",
        "संख्या१",
        "_चर",
        "test",
        "abc",
        "१२३"
    ]

    print("शब्द परीक्षण:")

    for शब्द in परीक्षण_सूची:

        if प्रणाली.मान्य(शब्द):

            print(शब्द, "मान्य")

        else:

            print(शब्द, "अमान्य")
