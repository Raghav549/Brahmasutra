import सूत्र_भाषा_निष्पादन_यन्त्र as सूत्र


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global यन्त्र


    यन्त्र = सूत्र.सूत्रयन्त्र()

    यन्त्र.निष्पादन("परीक्षण.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
