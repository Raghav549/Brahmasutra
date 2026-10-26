from सूत्र_स्वविकास_कृत्रिमबुद्धि import सूत्रस्वविकासकृत्रिमबुद्धि


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global AI

    AI = सूत्रस्वविकासकृत्रिमबुद्धि()

    AI.निरंतर()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
