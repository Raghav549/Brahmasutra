from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU
from सूत्र_binary_generator import सूत्रBinaryGenerator
from सूत्र_binary_loader import सूत्रBinaryLoader


program = [

    "स्थापित अ 100",
    "स्थापित ब 25",
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
    global cpu, encoder, generator, loaded_machine, loader, machine


    encoder = सूत्रMachineCode()

    machine = encoder.encode(program)


    generator = सूत्रBinaryGenerator()

    generator.save(machine, "test.bin")


    loader = सूत्रBinaryLoader()

    loaded_machine = loader.load("test.bin")


    cpu = सूत्रMachineCPU()

    cpu.run(loaded_machine)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
