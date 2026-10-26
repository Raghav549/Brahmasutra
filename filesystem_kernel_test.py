from सूत्र_kernel_filesystem import सूत्रKernelFileSystem


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global fs


    fs = सूत्रKernelFileSystem()


    fs.create("app1.सूत्र", "print('Sanskrit App 1')")
    fs.create("app2.सूत्र", "print('Sanskrit App 2')")


    fs.list()


    fs.read("app1.सूत्र")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
