import सूत्र_hardware_privilege as hw


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cpu


    cpu = hw.सूत्र_CPU()


    cpu.स्तर_स्थिति()


    cpu.संरक्षित_आदेश()


    cpu.कर्ण_प्रवेश()


    cpu.स्तर_स्थिति()


    cpu.संरक्षित_आदेश()


    cpu.उपयोगकर्ता_प्रवेश()


    cpu.स्तर_स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
