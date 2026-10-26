# सूत्र तंत्र — ISA


निर्देश_समुच्चय = {

    "लोड": 1,
    "योग": 2,
    "गुण": 3,
    "दर्शय": 4

}


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र ISA सक्रिय")

    print("ISA तैयार")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
