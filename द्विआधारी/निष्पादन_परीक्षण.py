from सूत्र_द्विआधारी_निष्पादक import सूत्रद्विआधारीनिष्पादक


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    import os

    global निष्पादक

    # पथ को इस फ़ाइल के सापेक्ष हल करें — CWD पर निर्भर न रहें।
    यहाँ = os.path.dirname(os.path.abspath(__file__))
    संचिका = os.path.join(यहाँ, "परीक्षण.द्विआधारी")

    निष्पादक = सूत्रद्विआधारीनिष्पादक()

    निष्पादक.निष्पादन(संचिका)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
