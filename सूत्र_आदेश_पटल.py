# =========================================
# सूत्र तंत्र — आदेश पटल (Shell)
# =========================================



import os


सक्रिय = True


def सहायता():

    print("उपलब्ध आदेश:")

    print("दर्शय          → वर्तमान स्थान")
    print("सूची           → संचिका सूची")
    print("निर्माण नाम     → संचिका निर्माण")
    print("लिख नाम        → संचिका में लिखो")
    print("पढ़ नाम        → संचिका पढ़ो")
    print("मिटा नाम       → संचिका हटाओ")
    print("निर्गम         → Shell बन्द")


def स्थान():

    print("स्थान:", os.getcwd())


def सूची():

    संचिकाएँ = os.listdir()

    print("संचिका सूची:")

    for स in संचिकाएँ:

        print("•", स)


def निर्माण(नाम):

    with open(नाम, "w", encoding="utf-8") as f:

        pass

    print("संचिका निर्मित:", नाम)


def लिख(नाम):

    लेख = input("लिखो: ")

    with open(नाम, "w", encoding="utf-8") as f:

        f.write(लेख)

    print("लिखित")


def पढ़(नाम):

    try:

        with open(नाम, "r", encoding="utf-8") as f:

            print(f.read())

    except:

        print("संचिका नहीं मिली")


def मिटा(नाम):

    try:

        os.remove(नाम)

        print("संचिका मिटाई")

    except:

        print("संचिका नहीं मिली")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश, भाग
    print("🕉️ सूत्र आदेश पटल सक्रिय")
    print("आदेश लिखत: सहायता")


    while सक्रिय:

        आदेश = input("सूत्र >>> ")

        भाग = आदेश.split()

        if len(भाग) == 0:
            continue


        if भाग[0] == "निर्गम":

            print("सूत्र Shell बन्द")

            break


        elif भाग[0] == "सहायता":

            सहायता()


        elif भाग[0] == "दर्शय":

            स्थान()


        elif भाग[0] == "सूची":

            सूची()


        elif भाग[0] == "निर्माण":

            निर्माण(भाग[1])


        elif भाग[0] == "लिख":

            लिख(भाग[1])


        elif भाग[0] == "पढ़":

            पढ़(भाग[1])


        elif भाग[0] == "मिटा":

            मिटा(भाग[1])


        else:

            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
