from सूत्र_स्वायत्त_कृत्रिमबुद्धि import सूत्रस्वायत्तकृत्रिमबुद्धि


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    """तीन चक्र चलाकर रुकें — पहले यह अनंत लूप में चलता रहता था।"""
    global AI

    AI = सूत्रस्वायत्तकृत्रिमबुद्धि()

    for _ in range(3):
        AI.चक्र()

    AI.बन्द()
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
