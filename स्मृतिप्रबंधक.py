# सूत्र तंत्र — स्मृति प्रबंधक
# पूर्णतः संस्कृत आधारित Memory Manager


# कुल स्मृति (bytes में)
कुल_स्मृति = 1024

# स्मृति array
स्मृति = [0] * कुल_स्मृति

# allocation table
आवंटन = {}

# next free address
अगला_स्थान = 0


# allocate memory
def स्मृति_आवंटन(आकार):

    global अगला_स्थान

    if अगला_स्थान + आकार > कुल_स्मृति:

        print("त्रुटि: स्मृति पूर्ण")
        return None

    प्रारंभ = अगला_स्थान

    आवंटन[प्रारंभ] = आकार

    अगला_स्थान += आकार

    print("स्मृति आवंटित:", प्रारंभ, "से", प्रारंभ+आकार)

    return प्रारंभ


# free memory
def स्मृति_मुक्त(स्थान):

    if स्थान in आवंटन:

        आकार = आवंटन[स्थान]

        del आवंटन[स्थान]

        print("स्मृति मुक्त:", स्थान)

    else:

        print("त्रुटि: अमान्य स्थान")


# write memory
def स्मृति_लिखो(स्थान, मान):

    if स्थान < कुल_स्मृति:

        स्मृति[स्थान] = मान

        print("लिखा:", मान, "स्थान:", स्थान)

    else:

        print("त्रुटि: स्थान सीमा से बाहर")


# read memory
def स्मृति_पढ़ो(स्थान):

    if स्थान < कुल_स्मृति:

        मान = स्मृति[स्थान]

        print("पढ़ा:", मान)

        return मान

    else:

        print("त्रुटि: स्थान सीमा से बाहर")


# show memory map
def स्मृति_स्थिति():

    print("स्मृति आवंटन तालिका:")

    for स्थान in आवंटन:

        print("स्थान:", स्थान, "आकार:", आवंटन[स्थान])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global addr
    print("स्मृति प्रबंधक आरम्भ")


    # TEST

    addr = स्मृति_आवंटन(10)

    स्मृति_लिखो(addr, 99)

    स्मृति_पढ़ो(addr)

    स्मृति_स्थिति()

    स्मृति_मुक्त(addr)

    स्मृति_स्थिति()

    print("स्मृति प्रबंधक सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
