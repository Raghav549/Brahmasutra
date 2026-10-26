# सूत्र तंत्र — Kernel
# पूर्णतः संस्कृत आधारित Operating System core


# प्रक्रिया तालिका
प्रक्रियाएँ = {}

# प्रक्रिया ID generator
अगला_प्रक्रिया_ID = 1

# प्रक्रिया class
class प्रक्रिया:

    def __init__(self, नाम):
        global अगला_प्रक्रिया_ID

        self.ID = अगला_प्रक्रिया_ID
        अगला_प्रक्रिया_ID += 1

        self.नाम = नाम
        self.स्थिति = "नवीन"

    def चलाओ(self):
        self.स्थिति = "चल रही"
        print("प्रक्रिया चल रही:", self.नाम)

    def रोको(self):
        self.स्थिति = "रुकी"
        print("प्रक्रिया रुकी:", self.नाम)


# Kernel functions

def प्रक्रिया_निर्माण(नाम):

    p = प्रक्रिया(नाम)

    प्रक्रियाएँ[p.ID] = p

    print("प्रक्रिया निर्मित:", नाम, "ID:", p.ID)

    return p


def प्रक्रिया_चलाओ(ID):

    if ID in प्रक्रियाएँ:

        प्रक्रियाएँ[ID].चलाओ()

    else:

        print("त्रुटि: प्रक्रिया नहीं मिली")


def प्रक्रिया_रोको(ID):

    if ID in प्रक्रियाएँ:

        प्रक्रियाएँ[ID].रोको()

    else:

        print("त्रुटि: प्रक्रिया नहीं मिली")


def प्रक्रिया_सूची():

    print("सभी प्रक्रियाएँ:")

    for ID in प्रक्रियाएँ:

        p = प्रक्रियाएँ[ID]

        print("ID:", p.ID, "नाम:", p.नाम, "स्थिति:", p.स्थिति)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global p1, p2
    print("सूत्र कर्नेल आरम्भ")


    # Test kernel

    p1 = प्रक्रिया_निर्माण("गणना")
    p2 = प्रक्रिया_निर्माण("संग्रह")

    प्रक्रिया_चलाओ(p1.ID)
    प्रक्रिया_चलाओ(p2.ID)

    प्रक्रिया_रोको(p1.ID)

    प्रक्रिया_सूची()

    print("सूत्र कर्नेल सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
