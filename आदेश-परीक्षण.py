import सूत्र_आदेश_विश्लेषक as विश्लेषक


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global वि


    वि = विश्लेषक.आदेशविश्लेषक()


    वि.चलाओ("स्थापित अ 10")

    वि.चलाओ("स्थापित ब 20")

    वि.चलाओ("योग अ ब")

    वि.चलाओ("दर्शय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
