from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_executable_generator import सूत्रExecutableGenerator
from सूत्र_app_packager import सूत्रAppPackager
from सूत्र_app_loader import सूत्रAppLoader


program = [

    "स्थापित अ 1000",
    "स्थापित ब 500",
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
    global encoder, exe_gen, loader, machine, packager


    encoder = सूत्रMachineCode()

    machine = encoder.encode(program)


    exe_gen = सूत्रExecutableGenerator()

    exe_gen.create(machine, "app_exec.सूत्र")


    packager = सूत्रAppPackager()

    packager.package("app_exec.सूत्र", "calculator")


    loader = सूत्रAppLoader()

    loader.run("calculator.सूत्रapp")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
