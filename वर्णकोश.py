# सूत्र तंत्र — वर्ण-कोश

वर्णसूची = [

"अ","आ","इ","ई","उ","ऊ","ऋ","ॠ","ऌ","ए","ऐ","ओ","औ",

"क","ख","ग","घ","ङ",
"च","छ","ज","झ","ञ",
"ट","ठ","ड","ढ","ण",
"त","थ","द","ध","न",
"प","फ","ब","भ","म",
"य","र","ल","व",
"श","ष","स","ह",

"क्ष","त्र","ज्ञ",

"०","१","२","३","४","५","६","७","८","९",

"।","॥","ः","ं","ँ"

]

def वर्ण_मान्य(चिह्न):
    return चिह्न in वर्णसूची


def परीक्षण():

    print("सूत्र वर्ण-कोश सक्रिय")

    परीक्षण_वर्ण = "क"

    if वर्ण_मान्य(परीक्षण_वर्ण):
        print("मान्य वर्ण:", परीक्षण_वर्ण)
    else:
        print("अमान्य वर्ण")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    परीक्षण()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
