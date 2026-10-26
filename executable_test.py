from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU
from सूत्र_executable_generator import सूत्रExecutableGenerator
from सूत्र_executable_loader import सूत्रExecutableLoader


program = [

    "स्थापित अ 500",
    "स्थापित ब 250",
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
    global cpu, encoder, generator, loaded, loader, machine


    encoder = सूत्रMachineCode()

    machine = encoder.encode(program)


    generator = सूत्रExecutableGenerator()

    generator.create(machine, "hello.सूत्र")


    loader = सूत्रExecutableLoader()

    loaded = loader.load("hello.सूत्र")


    cpu = सूत्रMachineCPU()

    cpu.run(loaded)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
