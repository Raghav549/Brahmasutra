# 🕉️ सूत्र पूर्ण स्वदेशी संचालन मोड


import सूत्र_कर्ण_v2 as कर्ण
import सूत्र_shell_v2 as शेल


class संचालनमोड:


    def __init__(self):

        print("🕉️ सूत्र पूर्ण स्वदेशी संचालन मोड सक्रिय")


    def प्रारम्भ(self):

        print("कर्ण प्रारम्भ हो रहा है...")
        कर्ण.प्रारम्भ()

        print("शेल प्रारम्भ हो रहा है...")
        शेल.प्रारम्भ()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global प्रणाली
    प्रणाली = संचालनमोड()

    प्रणाली.प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
