import सूत्र_process_object as प्रक्रिया


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global उपयोगकर्ता, कर्ण


    कर्ण = प्रक्रिया.प्रक्रिया("कर्ण", "कर्ण")

    उपयोगकर्ता = प्रक्रिया.प्रक्रिया("एप", "उपयोगकर्ता")


    कर्ण.स्थिति()

    उपयोगकर्ता.स्थिति()


    कर्ण.स्मृति_स्थापित("root", "protected")

    उपयोगकर्ता.स्मृति_स्थापित("hack", "fail")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
