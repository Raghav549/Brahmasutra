# सूत्र तंत्र — Desktop Environment




# apps
अनुप्रयोग = []



# files
सञ्चिका = {}



# open app
def अनुप्रयोग_आरम्भ(नाम):

    अनुप्रयोग.append(नाम)

    print("अनुप्रयोग आरम्भ:", नाम)



# list apps
def अनुप्रयोग_सूची():

    print("सक्रिय अनुप्रयोग:")

    for app in अनुप्रयोग:

        print(app)



# create file
def सञ्चिका_निर्माण(नाम, सामग्री):

    सञ्चिका[नाम] = सामग्री

    print("सञ्चिका निर्मित:", नाम)



# read file
def सञ्चिका_पठन(नाम):

    if नाम in सञ्चिका:

        print("सामग्री:", सञ्चिका[नाम])

    else:

        print("सञ्चिका नहीं मिली")



# show desktop
def desktop():

    print("सूत्र Desktop सक्रिय")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Desktop आरम्भ")
    desktop()

    अनुप्रयोग_आरम्भ("calculator")

    अनुप्रयोग_आरम्भ("editor")

    अनुप्रयोग_सूची()

    सञ्चिका_निर्माण("test.txt", "नमस्ते सूत्र")

    सञ्चिका_पठन("test.txt")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
