from सूत्र_process_manager_v2 import सूत्रProcessManager
from सूत्र_scheduler import सूत्रScheduler


code1 = '''
print("App 1 running")
'''

code2 = '''
print("App 2 running")
'''

code3 = '''
print("AI engine running")
'''


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager, pid1, pid2, pid3, scheduler


    manager = सूत्रProcessManager()
    scheduler = सूत्रScheduler()


    pid1 = manager.create(code1)
    pid2 = manager.create(code2)
    pid3 = manager.create(code3)


    scheduler.add_process(manager.processes[pid1])
    scheduler.add_process(manager.processes[pid2])
    scheduler.add_process(manager.processes[pid3])


    scheduler.run()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
