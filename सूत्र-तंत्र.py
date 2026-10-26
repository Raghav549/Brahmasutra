# =========================================
# सूत्र तंत्र v1 — मुख्य नियंत्रण केंद्र
# =========================================

import time


def यन्त्र_लोड():

    print("यन्त्र स्तर लोड...")

    import सूत्र_यन्त्र_स्तर

    time.sleep(1)


def कर्ण_लोड():

    print("कर्ण लोड...")

    import सूत्र_कर्ण_मूल

    time.sleep(1)


def Shell_लोड():

    print("आदेश पटल लोड...")

    import सूत्र_आदेश_पटल

    time.sleep(1)


def भाषा_लोड():

    print("सूत्र भाषा तैयार")

    import सूत्र_भाषा


def तंत्र_प्रारम्भ():

    यन्त्र_लोड()

    कर्ण_लोड()

    Shell_लोड()

    भाषा_लोड()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र तंत्र v1 स्थिर संस्करण")
    print("प्रारम्भ हो रहा है...")
    time.sleep(1)


    # Start system
    तंत्र_प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
