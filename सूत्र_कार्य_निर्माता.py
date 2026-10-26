
class कार्यनिर्माता:

    def निर्मित(self, input_binary, output_exec):

        with open(input_binary, "rb") as f:
            data = f.read()

        header = b"SUTRA_EXEC_V1"

        with open(output_exec, "wb") as f:

            f.write(header)
            f.write(data)

        print("कार्य निर्मित:", output_exec)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ सूत्र कार्य निर्माता सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
