# 🕉️ सूत्र निष्पादन प्रणाली (VERSION 4 FINAL)



# चर संग्रह
चर = {}


# वाक्य निष्पादन function
def निष्पादय(वाक्य):

    भाग = वाक्य.strip().split()

    if len(भाग) == 0:
        return


    # संकल्प (variable creation)
    if भाग[0] == "संकल्प":

        नाम = भाग[1]
        मान = int(भाग[2])

        चर[नाम] = मान

        print(f"संकल्प: {नाम} = {मान}")



    # योग (addition)
    elif भाग[0] == "योग":

        अ = भाग[1]
        ब = भाग[2]

        if अ in चर and ब in चर:

            चर[अ] = चर[अ] + चर[ब]

            print(f"योग: {अ} = {चर[अ]}")

        else:

            print("त्रुटि: चर नहीं मिला")



    # दर्शय (print)
    elif भाग[0] == "दर्शय":

        नाम = भाग[1]

        if नाम in चर:

            print(f"दर्शय: {नाम} = {चर[नाम]}")

        else:

            print("त्रुटि: चर नहीं मिला")



    else:

        print("त्रुटि: अमान्य वाक्य")



# परीक्षण कार्यक्रम
कार्यक्रम = [

    "संकल्प अ 10",
    "संकल्प ब 20",
    "योग अ ब",
    "दर्शय अ"

]


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global वाक्य
    print("🕉️ सूत्र वर्ण प्रणाली सक्रिय")
    print("🕉️ सूत्र शब्द प्रणाली सक्रिय")
    print("🕉️ सूत्र वाक्य प्रणाली सक्रिय")
    print("🕉️ सूत्र निष्पादन प्रणाली सक्रिय")



    # निष्पादन
    for वाक्य in कार्यक्रम:

        निष्पादय(वाक्य)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
