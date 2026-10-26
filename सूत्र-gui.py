# सूत्र तंत्र — GUI Kernel




# window list
खिड़की_सूची = []



# create window
def खिड़की_निर्माण(नाम):

    window = {

        "नाम": नाम,

        "स्थिति": "सक्रिय"

    }

    खिड़की_सूची.append(window)

    print("खिड़की निर्मित:", नाम)



# show windows
def खिड़की_सूची_दर्शय():

    print("सक्रिय खिड़कियाँ:")

    for w in खिड़की_सूची:

        print(w["नाम"], "-", w["स्थिति"])



# close window
def खिड़की_बंद(नाम):

    for w in खिड़की_सूची:

        if w["नाम"] == नाम:

            w["स्थिति"] = "बंद"

            print("खिड़की बंद:", नाम)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र GUI आरम्भ")
    खिड़की_निर्माण("editor")

    खिड़की_निर्माण("calculator")

    खिड़की_सूची_दर्शय()

    खिड़की_बंद("editor")

    खिड़की_सूची_दर्शय()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
