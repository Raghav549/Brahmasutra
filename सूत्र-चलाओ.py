# =========================================
# सूत्र भाषा — संचिका निष्पादन प्रणाली
# =========================================

import sys


चर = {}


def दर्शय(नाम):

    if नाम in चर:

        print(नाम, "=", चर[नाम])

    else:

        print("अज्ञात चर:", नाम)


def स्थापय(नाम, मान):

    चर[नाम] = int(मान)


def योग(क, ख):

    चर[क] += चर[ख]


def घटा(क, ख):

    चर[क] -= चर[ख]


def गुण(क, ख):

    चर[क] *= चर[ख]


def आदेश_चलाओ(पंक्ति):

    भाग = पंक्ति.strip().split()

    if len(भाग) == 0:
        return


    आदेश = भाग[0]


    if आदेश == "स्थापय":

        स्थापय(भाग[1], भाग[2])


    elif आदेश == "योग":

        योग(भाग[1], भाग[2])


    elif आदेश == "घटा":

        घटा(भाग[1], भाग[2])


    elif आदेश == "गुण":

        गुण(भाग[1], भाग[2])


    elif आदेश == "दर्शय":

        दर्शय(भाग[1])


    else:

        print("अज्ञात आदेश:", आदेश)


def संचिका_चलाओ(नाम):

    try:

        with open(नाम, "r", encoding="utf-8") as f:

            पंक्तियाँ = f.readlines()


        print("कार्यक्रम प्रारम्भ")

        for पंक्ति in पंक्तियाँ:

            आदेश_चलाओ(पंक्ति)


        print("कार्यक्रम समाप्त")


    except:

        print("संचिका नहीं मिली")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ सूत्र संचिका निष्पादक सक्रिय")


    if len(sys.argv) < 2:

        print("उपयोग:")
        print("python सूत्र-चलाओ.py कार्यक्रम.सूत्र")

    else:

        संचिका_चलाओ(sys.argv[1])


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
