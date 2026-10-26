from सूत्र_अनुप्रयोग_निर्माता import सूत्रअनुप्रयोगनिर्माता


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global निर्माता

    निर्माता = सूत्रअनुप्रयोगनिर्माता()

    निर्माता.सूत्र_अनुप्रयोग_निर्माण("मेरा_अनुप्रयोग")

    निर्माता.वेबसाइट_निर्माण("मेरा_वेबसाइट")

    निर्माता.स्वचालन_निर्माण("मेरा_स्वचालन")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
