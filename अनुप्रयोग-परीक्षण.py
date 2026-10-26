import सूत्र_अनुप्रयोग_निष्पादन as अनुप्रयोग


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global गणना, तंत्र, स्मृति


    तंत्र = अनुप्रयोग.अनुप्रयोगतंत्र()


    गणना = तंत्र.लोड("गणना", [

        "संकल्प अ 10",

        "संकल्प ब 20",

        "योग अ ब",

        "दर्शय अ"

    ])


    स्मृति = तंत्र.लोड("स्मृति", [

        "स्मृति आवंटन 1024",

        "स्मृति स्थिति"

    ])


    तंत्र.निष्पादन("गणना")

    तंत्र.निष्पादन("स्मृति")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
