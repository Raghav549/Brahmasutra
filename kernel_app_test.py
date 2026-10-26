from सूत्र_kernel_app_layer import सूत्रKernelAppLayer


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global kernel


    kernel = सूत्रKernelAppLayer()


    kernel.install_app("calculator.सूत्रapp")


    kernel.list_apps()


    kernel.run_app("calculator.सूत्रapp")


    kernel.remove_app("calculator.सूत्रapp")


    kernel.list_apps()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
