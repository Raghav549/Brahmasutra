from सूत्र_प्रक्रिया_पृथक्करण import सूत्रप्रक्रियापृथक्करण


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager


    manager = सूत्रप्रक्रियापृथक्करण()


    manager.निर्माण("ऐप१")

    manager.निर्माण("ऐप२")

    manager.निर्माण("ऐप३")


    manager.सूची()


    manager.समाप्त("ऐप२")


    manager.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
