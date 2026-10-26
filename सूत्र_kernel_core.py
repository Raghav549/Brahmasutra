# सूत्र तंत्र — Kernel Core




प्रक्रिया_सूची = {}

PID = 0



def प्रक्रिया_निर्माण(नाम):

    global PID

    PID += 1

    प्रक्रिया_सूची[PID] = नाम

    print("नई प्रक्रिया:", PID, नाम)



def प्रक्रिया_दर्शय():

    for pid in प्रक्रिया_सूची:

        print(pid, प्रक्रिया_सूची[pid])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Kernel Core सक्रिय")



    प्रक्रिया_निर्माण("init")
    प्रक्रिया_निर्माण("shell")

    प्रक्रिया_दर्शय()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
