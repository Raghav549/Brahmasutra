# सूत्र तंत्र — REPL (Real-time Sanskrit Console)

from निर्वाहक import निर्वाह


def सूत्र_REPL():

    print("🕉️ सूत्र REPL सक्रिय")
    print("निर्गच्छ लिखकर बाहर जाएं")

    while True:

        आदेश = input("सूत्र> ")

        आदेश = आदेश.strip()

        if आदेश == "निर्गच्छ":

            print("सूत्र समाप्त")
            break

        if आदेश == "":
            continue

        try:

            निर्वाह(आदेश)

        except Exception as त्रुटि:

            print("त्रुटि:", त्रुटि)


def परीक्षण():

    सूत्र_REPL()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    परीक्षण()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
