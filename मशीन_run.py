# 🕉️ सूत्र Machine Run

import सूत्र_machine_executor as executor


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cpu, file


    print("🕉️ सूत्र Machine Mode सक्रिय")

    file = input("संचिका नाम: ")

    cpu = executor.सूत्रMachineExecutor()

    cpu.run_file(file)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
