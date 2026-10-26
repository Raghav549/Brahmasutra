import सूत्र_प्रक्रिया_तंत्र as प्रक्रियातंत्र
import सूत्र_अनुसूचक_तंत्र as अनुसूचक


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global अनु, प्रबंधक, प्र१, प्र२, प्र३


    प्रबंधक = प्रक्रियातंत्र.प्रक्रियातंत्र()

    अनु = अनुसूचक.अनुसूचक()


    प्र१ = प्रबंधक.निर्माण("गणना")
    प्र२ = प्रबंधक.निर्माण("स्मृति")
    प्र३ = प्रबंधक.निर्माण("यन्त्र")


    अनु.प्रक्रिया_जोड़ो(प्र१)
    अनु.प्रक्रिया_जोड़ो(प्र२)
    अनु.प्रक्रिया_जोड़ो(प्र३)


    अनु.चलाओ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
