from सूत्र_यन्त्र_चालक import यन्त्रचालक
from सूत्र_कुंजीपटल_चालक import कुंजीपटल_पठन
from सूत्र_प्रदर्शन_चालक import प्रदर्शन_लेखन


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global driver, text


    driver = यन्त्रचालक()


    driver.पंजीकरण("कुंजीपटल", कुंजीपटल_पठन)
    driver.पंजीकरण("प्रदर्शन", प्रदर्शन_लेखन)


    text = driver.उपयोग("कुंजीपटल")

    driver.उपयोग("प्रदर्शन", text)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
