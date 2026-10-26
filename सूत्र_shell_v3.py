# 🕉️ सूत्र Shell v3

import सूत्र_स्मृति_प्रबंधक as स्मृति
import सूत्र_प्रक्रिया_तंत्र as प्रक्रिया
import सूत्र_सञ्चिका_तंत्र as सञ्चिका
import सूत्र_यन्त्र_तंत्र as यन्त्र


class Shell:


    def __init__(self):

        print("🕉️ सूत्र Shell v3 सक्रिय")


    def चलाओ(self):

        while True:

            आदेश = input("सूत्र >>> ")

            if आदेश == "निर्गम":

                print("Shell बन्द")

                break


            elif आदेश == "स्मृति":

                स्मृति.प्रारम्भ()


            elif आदेश == "प्रक्रिया":

                प्रक्रिया.प्रारम्भ()


            elif आदेश == "सञ्चिका":

                सञ्चिका.प्रारम्भ()


            elif आदेश == "यन्त्र":

                यन्त्र.प्रारम्भ()


            else:

                print("अज्ञात आदेश")



def प्रारम्भ(interactive=None, ऐप=None):
    """Start the shell.

    With ``interactive=False`` (or when stdin is not a terminal) the shell only
    reports that it is ready instead of blocking on ``input()`` — that is what
    the boot sequence needs.
    """
    import sys

    shell = Shell()

    if interactive is None:
        interactive = bool(sys.stdin and sys.stdin.isatty())

    if not interactive:
        print("🕉️ Shell तैयार (इंटरैक्टिव नहीं — input उपलब्ध नहीं)")
        return shell

    shell.चलाओ()
    return shell


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():



    # auto start (interactive only when a terminal is attached)
    प्रारम्भ()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
