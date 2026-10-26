# =========================================
# सूत्र तंत्र — आदेश निष्पादक
# =========================================



रजिस्टर = {

    "अ": 0,
    "ब": 0,
    "स": 0,
    "द": 0

}


def दर्शय():

    print("रजिस्टर स्थिति:")

    for नाम in रजिस्टर:

        print(नाम, "=", रजिस्टर[नाम])


def निष्पादय(पंक्ति):

    भाग = पंक्ति.split()

    if len(भाग) == 0:
        return


    यदि = भाग[0]


    if यदि == "स्थापय":

        नाम = भाग[1]

        मान = int(भाग[2])

        रजिस्टर[नाम] = मान

        print("स्थापित:", नाम, मान)


    elif यदि == "योग":

        लक्ष्य = भाग[1]

        स्रोत = भाग[2]

        रजिस्टर[लक्ष्य] += रजिस्टर[स्रोत]

        print("योग पूर्ण")


    elif यदि == "घटा":

        लक्ष्य = भाग[1]

        स्रोत = भाग[2]

        रजिस्टर[लक्ष्य] -= रजिस्टर[स्रोत]

        print("घटाव पूर्ण")


    elif यदि == "गुण":

        लक्ष्य = भाग[1]

        स्रोत = भाग[2]

        रजिस्टर[लक्ष्य] *= रजिस्टर[स्रोत]

        print("गुणन पूर्ण")


    elif यदि == "दर्शय":

        दर्शय()


    else:

        print("अमान्य आदेश")


सक्रिय = True


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश
    print("🕉️ सूत्र आदेश निष्पादक सक्रिय")
    print("आदेश: सहायता")

    while सक्रिय:

        आदेश = input("सूत्र >>> ")

        if आदेश == "निर्गम":

            print("निष्पादक बन्द")

            break


        elif आदेश == "सहायता":

            print("उपलब्ध आदेश:")
            print("स्थापय अ 10")
            print("योग अ ब")
            print("घटा अ ब")
            print("गुण अ ब")
            print("दर्शय")
            print("निर्गम")


        else:

            निष्पादय(आदेश)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
