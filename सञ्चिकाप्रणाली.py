# सूत्र तंत्र — सञ्चिका प्रणाली
# Sanskrit File System


# file storage
सञ्चिकाएँ = {}


# file create
def सञ्चिका_निर्माण(नाम):

    if नाम in सञ्चिकाएँ:

        print("त्रुटि: सञ्चिका पहले से है")

        return

    सञ्चिकाएँ[नाम] = ""

    print("सञ्चिका बनी:", नाम)


# file write
def सञ्चिका_लिखो(नाम, सामग्री):

    if नाम not in सञ्चिकाएँ:

        print("त्रुटि: सञ्चिका नहीं मिली")

        return

    सञ्चिकाएँ[नाम] = सामग्री

    print("सञ्चिका लिखी:", नाम)


# file read
def सञ्चिका_पढ़ो(नाम):

    if नाम not in सञ्चिकाएँ:

        print("त्रुटि: सञ्चिका नहीं मिली")

        return

    print("सामग्री:", सञ्चिकाएँ[नाम])

    return सञ्चिकाएँ[नाम]


# file delete
def सञ्चिका_मिटाओ(नाम):

    if नाम not in सञ्चिकाएँ:

        print("त्रुटि: सञ्चिका नहीं मिली")

        return

    del सञ्चिकाएँ[नाम]

    print("सञ्चिका मिटाई:", नाम)


# list files
def सञ्चिका_सूची():

    print("सञ्चिका सूची:")

    for नाम in सञ्चिकाएँ:

        print("-", नाम)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सञ्चिका प्रणाली आरम्भ")


    # TEST

    सञ्चिका_निर्माण("test.txt")

    सञ्चिका_लिखो("test.txt", "नमस्ते सूत्र")

    सञ्चिका_पढ़ो("test.txt")

    सञ्चिका_सूची()

    सञ्चिका_मिटाओ("test.txt")

    सञ्चिका_सूची()

    print("सञ्चिका प्रणाली सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
