import सूत्र_cpu_core as cpu


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global प्र


    प्र = cpu.सूत्रCPU()

    प्र.स्थापित("अ", 10)

    प्र.स्थापित("ब", 20)

    प्र.योग("अ", "ब")

    प्र.दर्शय()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
