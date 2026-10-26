# सूत्र तंत्र — दृश्य तंत्र
# Sanskrit GUI Engine


# window registry
विंडोसूची = {}



# create window
def विंडो_निर्माण(नाम):

    विंडोसूची[नाम] = {

        "नाम": नाम,
        "स्थिति": "दृश्य"

    }

    print("विंडो बनी:", नाम)



# draw text
def पाठ_दिखाओ(विंडो, पाठ):

    if विंडो not in विंडोसूची:

        print("त्रुटि: विंडो नहीं मिली")

        return

    print("[", विंडो, "]", पाठ)



# create button
def बटन_निर्माण(विंडो, नाम):

    if विंडो not in विंडोसूची:

        print("त्रुटि: विंडो नहीं मिली")

        return

    print("बटन बना:", नाम, "विंडो:", विंडो)



# close window
def विंडो_समाप्त(नाम):

    if नाम not in विंडोसूची:

        print("त्रुटि: विंडो नहीं मिली")

        return

    del विंडोसूची[नाम]

    print("विंडो बंद:", नाम)



# show windows
def विंडो_सूची():

    print("विंडो सूची:")

    for नाम in विंडोसूची:

        print("-", नाम)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("दृश्य तंत्र आरम्भ")



    # TEST

    विंडो_निर्माण("मुख्य")

    पाठ_दिखाओ("मुख्य", "नमस्ते सूत्र OS")

    बटन_निर्माण("मुख्य", "ठीक")

    विंडो_सूची()

    विंडो_समाप्त("मुख्य")

    विंडो_सूची()

    print("दृश्य तंत्र सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
