import सूत्र_उपयोगकर्ता_निष्पादन as उपयोगकर्ता


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global कार्य१, कार्य२, तंत्र


    तंत्र = उपयोगकर्ता.उपयोगकर्तातंत्र()


    कार्य१ = तंत्र.निर्माण("गणना")

    कार्य२ = तंत्र.निर्माण("स्मृति")


    तंत्र.निष्पादन(कार्य१)

    तंत्र.निष्पादन(कार्य२)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
