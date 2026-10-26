from सूत्र_interrupt_manager import सूत्रInterruptManager


def keyboard_interrupt():

    print("Keyboard interrupt handled")


def system_call_interrupt():

    print("System call interrupt handled")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager


    manager = सूत्रInterruptManager()


    manager.register("KEYBOARD", keyboard_interrupt)

    manager.register("SYSCALL", system_call_interrupt)


    manager.trigger("KEYBOARD")

    manager.trigger("SYSCALL")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
