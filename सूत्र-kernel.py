# सूत्र तंत्र — Kernel Core




# process table
प्रक्रिया_तालिका = {}



# memory
स्मृति = {}



# process id counter
अगला_PID = 1



# create process
def प्रक्रिया_निर्माण(नाम):

    global अगला_PID

    PID = अगला_PID

    प्रक्रिया_तालिका[PID] = नाम

    अगला_PID += 1

    print("प्रक्रिया निर्मित:", नाम, "PID:", PID)

    return PID



# list processes
def प्रक्रिया_सूची():

    print("सक्रिय प्रक्रियाएँ:")

    for pid in प्रक्रिया_तालिका:

        print(pid, प्रक्रिया_तालिका[pid])



# memory write
def स्मृति_लिखो(स्थान, मान):

    स्मृति[स्थान] = मान

    print("स्मृति लिखित:", स्थान, मान)



# memory read
def स्मृति_पढ़ो(स्थान):

    if स्थान in स्मृति:

        print("स्मृति मान:", स्मृति[स्थान])

    else:

        print("स्थान रिक्त")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global pid1, pid2
    print("सूत्र Kernel आरम्भ")
    pid1 = प्रक्रिया_निर्माण("calculator")

    pid2 = प्रक्रिया_निर्माण("editor")

    प्रक्रिया_सूची()

    स्मृति_लिखो("A", 100)

    स्मृति_पढ़ो("A")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
