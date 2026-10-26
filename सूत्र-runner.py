# सूत्र तंत्र — सूत्र Executable Runner




HEADER = "सूत्रEXEC"



# memory
चर = {}



def run_executable(file):

    with open(file, "r", encoding="utf-8") as f:

        lines = f.readlines()


    if lines[0].strip() != HEADER:

        print("त्रुटि: अमान्य executable")

        return


    for line in lines[1:]:

        parts = line.strip().split()

        if len(parts) == 0:
            continue


        cmd = parts[0]


        if cmd == "SET":

            चर[parts[1]] = int(parts[2])

            print("SET:", parts[1], "=", parts[2])


        elif cmd == "ADD":

            result = चर[parts[1]] + चर[parts[2]]

            print("ADD result:", result)


        elif cmd == "MUL":

            result = चर[parts[1]] * चर[parts[2]]

            print("MUL result:", result)


        elif cmd == "PRINT":

            print("PRINT:", चर[parts[1]])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र runner सक्रिय")
    run_executable("program.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
