from सूत्र_अनुसूचक import सूत्रअनुसूचक


def कार्य१():

    print("ऐप१ चल रहा है")


def कार्य२():

    print("ऐप२ चल रहा है")


def कार्य३():

    print("ऐप३ चल रहा है")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global scheduler


    scheduler = सूत्रअनुसूचक()

    scheduler.जोड़("ऐप१", कार्य१)

    scheduler.जोड़("ऐप२", कार्य२)

    scheduler.जोड़("ऐप३", कार्य३)


    scheduler.चलाओ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
