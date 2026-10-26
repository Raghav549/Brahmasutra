

# --- headless-safe input -----------------------------------------------------
# These demos read from a terminal.  Under CI, `nohup` or the legacy baseline
# there is no terminal, and a raw `input()` raises EOFError (exit 1) or spins.
# `_इनपुट` behaves like `input()` interactively and stops cleanly otherwise.
_EOF_गिनती = {"n": 0}


def _इनपुट(prompt=""):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        _EOF_गिनती["n"] += 1
        if _EOF_गिनती["n"] > 1:
            raise SystemExit(0)
        return "निर्गम"




# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cmd
    print("🕉️ ~/सूत्र-तंत्र/सर्वनिर्माण_v14/mahadevAI/frontend Backend Active")

    while True:

        cmd = _इनपुट("server> ")

        if cmd=="exit":
            break

        print("processed:",cmd)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
