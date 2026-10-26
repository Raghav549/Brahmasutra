# 🕉️ सूत्र Mode Test

import सूत्र_kernel_mode as कर्ण
import सूत्र_user_mode as उपयोगकर्ता


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("कर्ण प्रारम्भ हो रहा है...")
    कर्ण.प्रारम्भ()


    print("उपयोगकर्ता प्रारम्भ हो रहा है...")
    उपयोगकर्ता.प्रारम्भ()


    print("प्रणाली आह्वान परीक्षण")
    उपयोगकर्ता.प्रणाली_आह्वान("स्मृति_स्थिति")

    उपयोगकर्ता.प्रणाली_आह्वान("यन्त्र_स्थिति")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
