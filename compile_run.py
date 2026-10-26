


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard so that importing this module
# has no side effects (see tools/harden_imports.py and docs/AUDIT.md).
# ---------------------------------------------------------------------------
def _main():
    global argv, c, output, source, मुख्य
    """Source → binary compiler driver.
    
    Prompts only when run as a script; importing the module is side-effect free.
    """
    
    import sys
    
    import सूत्र_full_compiler as compiler
    
    
    def मुख्य(argv=None):
        argv = list(sys.argv[1:] if argv is None else argv)
        if len(argv) >= 2:
            source, output = argv[0], argv[1]
        else:
            try:
                source = input("Source file: ").strip()
                output = input("Output binary: ").strip()
            except EOFError:
                print("उपयोग: python compile_run.py <source> <output>")
                return 2
        c = compiler.सूत्रCompiler()
        c.compile(source, output)
        return 0
    
    
    if __name__ == "__main__":
        raise SystemExit(मुख्य())


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
