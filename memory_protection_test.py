from सूत्र_process_manager_v2 import सूत्रProcessManager
from सूत्र_memory_protection import सूत्रMemoryProtection


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager, memory, pid1, pid2


    manager = सूत्रProcessManager()
    memory = सूत्रMemoryProtection()


    pid1 = manager.create("print('Process 1')")
    pid2 = manager.create("print('Process 2')")


    memory.allocate(pid1)
    memory.allocate(pid2)


    memory.write(pid1, "data", "secret_app1")
    memory.write(pid2, "data", "secret_app2")


    print("PID1 memory:", memory.read(pid1, "data"))
    print("PID2 memory:", memory.read(pid2, "data"))


    memory.show()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
