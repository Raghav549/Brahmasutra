# सूत्र तंत्र — उपकरण चालक प्रणाली
# Sanskrit Device Driver System


# device registry
उपकरणसूची = {}



# register device
def उपकरण_पंजीकरण(नाम):

    उपकरणसूची[नाम] = {

        "नाम": नाम,
        "स्थिति": "सक्रिय"

    }

    print("उपकरण पंजीकृत:", नाम)



# write device
def उपकरण_लिखो(नाम, डेटा):

    if नाम not in उपकरणसूची:

        print("त्रुटि: उपकरण नहीं मिला")

        return

    print("डेटा लिखा गया", नाम, ":", डेटा)



# read device
def उपकरण_पढ़ो(नाम):

    if नाम not in उपकरणसूची:

        print("त्रुटि: उपकरण नहीं मिला")

        return

    डेटा = "उदाहरण डेटा"

    print("डेटा पढ़ा गया", नाम, ":", डेटा)

    return डेटा



# show devices
def उपकरण_सूची():

    print("उपकरण सूची:")

    for नाम in उपकरणसूची:

        print("-", नाम)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("उपकरण चालक प्रणाली आरम्भ")



    # TEST

    उपकरण_पंजीकरण("प्रदर्शक")

    उपकरण_पंजीकरण("संग्रह")

    उपकरण_सूची()

    उपकरण_लिखो("प्रदर्शक", "नमस्ते")

    उपकरण_पढ़ो("संग्रह")

    print("उपकरण चालक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
