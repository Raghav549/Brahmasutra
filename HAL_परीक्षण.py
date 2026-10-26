from सूत्र_HAL import सूत्रHAL
from सूत्र_CPU_HAL import CPU
from सूत्र_स्मृति_HAL import स्मृति


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global cpu, hal, memory


    hal = सूत्रHAL()


    cpu = CPU()
    memory = स्मृति()


    hal.पंजीकरण("CPU", cpu)
    hal.पंजीकरण("स्मृति", memory)


    cpu.स्थापित("अ", 100)

    print("CPU मान:", cpu.प्राप्त("अ"))


    memory.लिख(0, 999)

    print("Memory मान:", memory.पढ़(0))


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
