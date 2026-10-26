# 🕉️ ब्रह्म वर्ण कोर VERSION 2 FIXED FULL



class ब्रह्मवर्णकोर:

    def __init__(self):

        # सभी संस्कृत वर्ण
        self.स्वर = [
            "अ","आ","इ","ई","उ","ऊ","ऋ","ॠ","ऌ","ॡ",
            "ए","ऐ","ओ","औ"
        ]

        self.व्यंजन = [
            "क","ख","ग","घ","ङ",
            "च","छ","ज","झ","ञ",
            "ट","ठ","ड","ढ","ण",
            "त","थ","द","ध","न",
            "प","फ","ब","भ","म",
            "य","र","ल","व",
            "श","ष","स","ह"
        ]

        self.मात्रा = [
            "ा","ि","ी","ु","ू","ृ","ॄ","ॢ","ॣ",
            "े","ै","ो","ौ","ं","ः","ँ","्"
        ]

        self.विशेष = [
            " ", "_", "\n", "\t"
        ]

        # सभी valid वर्ण
        self.सभी = (
            self.स्वर +
            self.व्यंजन +
            self.मात्रा +
            self.विशेष
        )

    # वर्ण valid है या नहीं
    def मान्य(self, वर्ण):

        if वर्ण in self.सभी:
            return True

        return False

    # वर्ण प्रकार बताओ
    def प्रकार(self, वर्ण):

        if वर्ण in self.स्वर:
            return "स्वर"

        if वर्ण in self.व्यंजन:
            return "व्यंजन"

        if वर्ण in self.मात्रा:
            return "मात्रा"

        if वर्ण in self.विशेष:
            return "विशेष"

        return "अमान्य"


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global कोर, परीक्षण, वर्ण
    print("🕉️ ब्रह्म वर्ण कोर सक्रिय")
    कोर = ब्रह्मवर्णकोर()

    परीक्षण = [
        "अ",
        "क",
        "ि",
        "्",
        "म",
        "A"
    ]

    for वर्ण in परीक्षण:

        print(वर्ण, "→", कोर.मान्य(वर्ण), कोर.प्रकार(वर्ण))


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
