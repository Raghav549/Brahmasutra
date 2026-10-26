from ब्रह्म_अनुप्रयोग_ढाँचा.मूल import ब्रह्मअनुप्रयोग
from ब्रह्म_अनुप्रयोग_ढाँचा.UI import बटन, पृष्ठ


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global app, btn, page

    app = ब्रह्मअनुप्रयोग("मेरा_ऐप")

    page = पृष्ठ("मुख्य")

    btn = बटन("लॉगिन")

    page.जोड़ो(btn)

    app.घटक_जोड़ो("मुख्य पृष्ठ")

    app.प्रारम्भ()

    page.दर्शय()

    app.स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
