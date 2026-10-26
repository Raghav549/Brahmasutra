from सूत्र_सञ्चिका_कर्ण import सूत्रसञ्चिकाकर्ण


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global data, fs


    fs = सूत्रसञ्चिकाकर्ण()


    fs.लेखन("परीक्षण.txt", "नमस्ते सूत्र OS")

    data = fs.पठन("परीक्षण.txt")

    print("डेटा:", data)


    fs.सूची()


    fs.विलोपन("परीक्षण.txt")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
