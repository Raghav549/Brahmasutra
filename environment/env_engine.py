import os

def प्रारंभ():

    print("====================================")
    print("     सूत्र-पर्यावरण प्रारंभ")
    print("====================================")

    print("")
    print("उपलब्ध प्रणालियाँ:")
    print("• संस्कृत Compiler")
    print("• संस्कृत APK Builder")
    print("• संस्कृत IDE")
    print("• सूत्र Store")
    print("• संस्कृत Runtime")

    print("")
    print("मुख्य आदेश:")

    print("सूत्र-ide       → IDE प्रारंभ")
    print("संस्कृत-build   → APK निर्माण")
    print("संस्कृत-compile → compile")
    print("सूत्र-store     → Store access")
    print("चलाओ           → program run")

    print("")
    print("सूत्र-पर्यावरण तैयार")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    प्रारंभ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
