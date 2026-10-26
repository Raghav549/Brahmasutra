# 🕉️ सूत्र OS Boot Entry


from सूत्र_boot_manager import सूत्रBootManager


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global boot


    print("🕉️ सूत्र OS Boot प्रारम्भ")


    boot = सूत्रBootManager()

    boot.boot()


if __name__ == "__main__":
    _main()
