# 🕉️ ब्रह्म AI प्रवेश तंत्र

class ब्रह्मप्रवेश:

    def __init__(self):
        print("🕉️ ब्रह्म AI प्रवेश तंत्र सक्रिय")

    def प्रवेश_ले(self):

        print("\nअपना आदेश लिखें:")
        आदेश = input(">>> ")

        return आदेश


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश, प्रवेश
    प्रवेश = ब्रह्मप्रवेश()

    आदेश = प्रवेश.प्रवेश_ले()

    print("\nप्राप्त आदेश:")
    print(आदेश)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
