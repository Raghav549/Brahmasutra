# 🕉️ BRAHMA VERSION 3
# सूत्र वाक्य प्रणाली

from सूत्र_शब्द import शब्दप्रणाली

print("🕉️ सूत्र वाक्य प्रणाली सक्रिय")

class वाक्यप्रणाली:

    def __init__(self):

        self.शब्द = शब्दप्रणाली()

        self.आदेश = [
            "संकल्प",
            "योग",
            "दर्शय",
            "निर्गम"
        ]

    def विश्लेषण(self, पंक्ति):

        भाग = पंक्ति.strip().split()

        if len(भाग) == 0:

            return False

        आदेश = भाग[0]

        if आदेश not in self.आदेश:

            return False

        for शब्द in भाग[1:]:

            if not self.शब्द.मान्य(शब्द):

                return False

        return True


# परीक्षण
if __name__ == "__main__":

    प्रणाली = वाक्यप्रणाली()

    परीक्षण = [
        "संकल्प अ 10",
        "संकल्प ब 20",
        "योग अ ब",
        "दर्शय अ",
        "निर्गम",
        "invalid test",
        "abc xyz"
    ]

    print("वाक्य परीक्षण:")

    for पंक्ति in परीक्षण:

        if प्रणाली.विश्लेषण(पंक्ति):

            print(पंक्ति, "मान्य")

        else:

            print(पंक्ति, "अमान्य")
