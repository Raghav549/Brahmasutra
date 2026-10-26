from सूत्र_आह्वान_तंत्र import सूत्रआह्वानतंत्र


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global syscall


    syscall = सूत्रआह्वानतंत्र()


    print(syscall.आह्वान("स्मृति","allocate 1024"))

    print(syscall.आह्वान("सञ्चिका","read file"))

    print(syscall.आह्वान("प्रक्रिया","create process"))


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
