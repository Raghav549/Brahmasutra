import सूत्र_प्रक्रिया_तंत्र as तंत्र


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global प्रबंधक, प्र१, प्र२, प्र३


    प्रबंधक = तंत्र.प्रक्रियातंत्र()


    प्र१ = प्रबंधक.निर्माण("गणना")

    प्र२ = प्रबंधक.निर्माण("स्मृति")

    प्र३ = प्रबंधक.निर्माण("यन्त्र")


    प्रबंधक.प्रारम्भ(1)

    प्रबंधक.प्रारम्भ(2)

    प्रबंधक.समाप्त(1)


    प्रबंधक.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
