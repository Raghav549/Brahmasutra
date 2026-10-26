import सूत्र_स्मृति_तंत्र as स्मृति


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global अ, प्रबंधक, ब, स


    प्रबंधक = स्मृति.स्मृतितंत्र()


    अ = प्रबंधक.आवंटन(1024)

    ब = प्रबंधक.आवंटन(2048)

    स = प्रबंधक.आवंटन(512)


    प्रबंधक.मुक्त(ब)


    प्रबंधक.स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
