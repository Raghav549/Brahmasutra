from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU


program = [

    "स्थापित अ 50",
    "स्थापित ब 20",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cpu, encoder, machine


    encoder = सूत्रMachineCode()

    machine = encoder.encode(program)


    cpu = सूत्रMachineCPU()

    cpu.run(machine)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
