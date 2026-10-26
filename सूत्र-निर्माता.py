# सूत्र तंत्र — सूत्र Executable Builder




HEADER = "सूत्रEXEC"



def executable_बनाओ(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:

        code = f.read()


    with open(output_file, "w", encoding="utf-8") as f:

        f.write(HEADER + "\n")

        f.write(code)


    print("Executable निर्मित:", output_file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र executable निर्माता सक्रिय")
    executable_बनाओ("program.sbc", "program.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
