import सूत्र_कर्ण_सञ्चिका_एकीकरण as कर्ण


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global प्रबंधक


    प्रबंधक = कर्ण.कर्णसञ्चिकातंत्र()


    प्रबंधक.आदेश("निर्माण test.txt")

    प्रबंधक.आदेश("लेखन test.txt नमस्ते सूत्र OS")

    प्रबंधक.आदेश("पठन test.txt")

    प्रबंधक.आदेश("सूची")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
