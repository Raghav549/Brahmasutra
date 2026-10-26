from सूत्र_हार्डवेयर_मशीन import सूत्रHardwareMachine

program = [

    {"opcode":"LOAD","op1":"अ","op2":100},

    {"opcode":"LOAD","op1":"ब","op2":200},

    {"opcode":"ADD","op1":"अ","op2":"ब"},

    {"opcode":"SHOW","op1":"अ"},

    {"opcode":"STATE"},

    {"opcode":"EXIT"}

]


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global machine

    machine = सूत्रHardwareMachine()

    machine.program_load(program)

    machine.execute()

    machine.status()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
