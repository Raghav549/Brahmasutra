# 🕉️ सूत्र सञ्चिका निष्पादन प्रणाली (VERSION 5)



चर = {}


def निष्पादय(वाक्य):

    भाग = वाक्य.strip().split()

    if len(भाग) == 0:
        return


    if भाग[0] == "संकल्प":

        नाम = भाग[1]
        मान = int(भाग[2])

        चर[नाम] = मान

        print(f"संकल्प: {नाम} = {मान}")



    elif भाग[0] == "योग":

        अ = भाग[1]
        ब = भाग[2]

        if अ in चर and ब in चर:

            चर[अ] = चर[अ] + चर[ब]

            print(f"योग: {अ} = {चर[अ]}")

        else:

            print("त्रुटि: चर नहीं मिला")



    elif भाग[0] == "दर्शय":

        नाम = भाग[1]

        if नाम in चर:

            print(f"दर्शय: {नाम} = {चर[नाम]}")

        else:

            print("त्रुटि: चर नहीं मिला")



    else:

        print("त्रुटि: अमान्य वाक्य")



# file execution
def सञ्चिका_चलाय(नाम):

    try:

        with open(नाम, "r", encoding="utf-8") as f:

            पंक्तियाँ = f.readlines()

            for पंक्ति in पंक्तियाँ:

                निष्पादय(पंक्ति)


    except:

        print("त्रुटि: सञ्चिका नहीं मिली")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ सूत्र सञ्चिका निष्पादन प्रणाली सक्रिय")



    # test execution
    सञ्चिका_चलाय("परीक्षण.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
