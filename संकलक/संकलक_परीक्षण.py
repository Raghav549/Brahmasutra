from सूत्र_संकलक import सूत्रसंकलक


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global संकलक

    import os as _os

    संकलक = सूत्रसंकलक()

    # पथ CWD पर नहीं, इस फ़ाइल की स्थिति पर आधारित होने चाहिए।
    मूल = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

    संकलक.संकलन(

    _os.path.join(मूल, "अनुप्रयोग", "परीक्षण.सूत्र"),

    _os.path.join(मूल, "द्विआधारी", "परीक्षण.द्विआधारी")

    )


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
