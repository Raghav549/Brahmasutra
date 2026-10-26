# सूत्र तंत्र — Operating System Execution Layer

import os
from सूत्रcompiler import compile_file
from सूत्रvm import सूत्रVM


def चलाओ(file):

    if not os.path.exists(file):

        print("त्रुटि: सञ्चिका नास्ति")
        return

    bytecode = file.replace(".sutra", ".sbc")

    print("संकलन आरम्भ...")

    compile_file(file, bytecode)

    print("संकलन सफल")

    print("कार्य निष्पादन आरम्भ...")

    vm = सूत्रVM()

    vm.run(bytecode)

    print("कार्य समाप्त")


def मुख्य():

    print("सूत्र तंत्र सक्रिय")

    while True:

        cmd = input("सूत्र >>> ")

        if cmd.startswith("run"):

            file = cmd.split(" ")[1]

            चलाओ(file)

        elif cmd == "निर्गम":

            print("सूत्र तंत्र बन्द")
            break

        else:

            print("अज्ञात आदेश")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    मुख्य()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
