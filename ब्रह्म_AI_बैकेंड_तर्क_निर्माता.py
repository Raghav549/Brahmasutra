# BRAHMA AUTO BACKEND LOGIC ENGINE

import os

from brahma_templates import write_chat_server

BASE = os.environ.get("BRAHMA_AI_ROOT") or os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")



class ब्रह्मबैकेंडनिर्माता:


    def निर्मित(self,name):

        path = f"{BASE}/{name}/backend"

        os.makedirs(path, exist_ok=True)


        written = write_chat_server(path, name)

        print("Backend logic निर्मित:", written)

        return written


BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_APPS")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global b, name

    print("🕉️ ब्रह्म बैकेंड तर्क निर्माता सक्रिय")


    os.makedirs(BASE, exist_ok=True)
    name = input("App name: ")

    b = ब्रह्मबैकेंडनिर्माता()

    b.निर्मित(name)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
