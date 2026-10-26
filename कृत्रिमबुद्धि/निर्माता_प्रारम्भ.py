from सूत्र_अनुप्रयोग_निर्माता import सूत्रअनुप्रयोगनिर्माता


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global AI, आदेश


    AI = सूत्रअनुप्रयोगनिर्माता()


    while True:

        आदेश = input("सूत्र निर्माता >>> ")

        if आदेश == "निर्गम":

            break

        elif आदेश == "सूत्र":

            AI.निर्माण("सूत्र")

        elif आदेश == "वेबसाइट":

            AI.निर्माण("वेबसाइट")

        elif आदेश == "स्वचालन":

            AI.निर्माण("स्वचालन")

        else:

            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
