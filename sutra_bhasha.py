# सूत्रभाषा Interpreter


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global app, text, आदेश
    print("🕉️ सूत्रभाषा सक्रिय")

    while True:
        आदेश = input("सूत्र >>> ")

        if आदेश.startswith("प्रदर्शय"):
            text = आदेश.replace("प्रदर्शय", "").strip()
            print(text)

        elif आदेश.startswith("उद्घाटय"):
            app = आदेश.replace("उद्घाटय", "").strip()
            print(f"{app} उद्घाटित")

        elif आदेश.startswith("निर्गच्छ"):
            print("सूत्रभाषा समाप्त")
            break

        else:
            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
