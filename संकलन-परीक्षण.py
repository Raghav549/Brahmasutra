import सूत्र_मूल_संकलक as संकलक

import सूत्र_संकलक as सं


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global स


    स = संकलक.मूलसंकलक()

    स.संकलन("परीक्षण.सूत्र", "परीक्षण.यन्त्र")


    स = सं.सूत्रसंकलक()

    स.संकलन("परीक्षण.सूत्र", "परीक्षण.यन्त्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
