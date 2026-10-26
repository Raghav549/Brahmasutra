import सूत्र_आह्वान_तंत्र as तंत्र
import सूत्र_आह्वान_कार्य as कार्य


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आह्वान


    आह्वान = तंत्र.आह्वानतंत्र()


    आह्वान.पंजीकरण("नमस्ते", कार्य.नमस्ते)

    आह्वान.पंजीकरण("योग", कार्य.योग)

    आह्वान.पंजीकरण("स्मृति", कार्य.स्मृति)


    आह्वान.आह्वान("नमस्ते")

    आह्वान.आह्वान("योग", 5, 7)

    आह्वान.आह्वान("स्मृति")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
