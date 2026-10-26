# 🕉️ BRAHMA VERSION 1
# सूत्र वर्ण प्रणाली


class वर्णप्रणाली:

    def __init__(self):

        self.स्वर = [
            "अ","आ","इ","ई","उ","ऊ",
            "ऋ","ॠ","ऌ","ॡ",
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

        self.संख्या = [
            "०","१","२","३","४",
            "५","६","७","८","९"
        ]

        self.विशेष = [
            "_"
        ]

        self.सर्व = (
            self.स्वर +
            self.व्यंजन +
            self.संख्या +
            self.विशेष
        )

    def मान्य(self, अक्षर):

        return अक्षर in self.सर्व


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global अक्षर, परीक्षण, प्रणाली
    print("🕉️ सूत्र वर्ण प्रणाली सक्रिय")
    प्रणाली = वर्णप्रणाली()

    print("मान्य वर्ण परीक्षण:")

    परीक्षण = ["अ","क","१","_","x"]

    for अक्षर in परीक्षण:

        if प्रणाली.मान्य(अक्षर):

            print(अक्षर, "मान्य")

        else:

            print(अक्षर, "अमान्य")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
