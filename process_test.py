from सूत्र_process_manager_v2 import सूत्रProcessManager


code1 = '''
x = 10
print("Process 1:", x)
'''

code2 = '''
x = 50
print("Process 2:", x)
'''


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager, pid1, pid2


    manager = सूत्रProcessManager()


    pid1 = manager.create(code1)
    pid2 = manager.create(code2)


    manager.run(pid1)
    manager.run(pid2)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
