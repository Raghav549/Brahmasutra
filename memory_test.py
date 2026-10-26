from सूत्र_memory_manager_v2 import सूत्रMemoryManagerV2


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global mem


    mem = सूत्रMemoryManagerV2()


    mem.allocate("process1", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


    mem.allocate("process2", "1234567890")


    mem.status()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
