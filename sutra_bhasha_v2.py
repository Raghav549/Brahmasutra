import os
import subprocess
import shutil
import time
import webbrowser


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global HOME, f, filename, files, parts, path, text, आदेश

    print("🕉️ सूत्रभाषा v2 सक्रिय")

    HOME = os.path.expanduser("~")

    while True:

        आदेश = input("सूत्र >>> ").strip()

        # प्रदर्शय = print
        if आदेश.startswith("प्रदर्शय"):
            text = आदेश.replace("प्रदर्शय", "").strip()
            print(text)


        # निर्मापय = create file
        elif आदेश.startswith("निर्मापय"):

            parts = आदेश.split()

            if len(parts) >= 2:

                filename = parts[1]
                path = os.path.join(HOME, filename)

                with open(path, "w") as f:
                    f.write("सूत्रभाषा द्वारा निर्मित")

                print(f"{filename} निर्मित")


        # उद्घाटय = open file
        elif आदेश.startswith("उद्घाटय"):

            parts = आदेश.split()

            if len(parts) >= 2:

                filename = parts[1]
                path = os.path.join(HOME, filename)

                _open_file(path)

                print(f"{filename} उद्घाटित")


        # सूची = list files
        elif आदेश == "सूची":

            files = os.listdir(HOME)

            for f in files:
                print(f)


        # समय = show time
        elif आदेश == "समय":

            print(time.strftime("%Y-%m-%d %H:%M:%S"))


        # स्वच्छ = clear screen
        elif आदेश == "स्वच्छ":

            print("\033[H\033[J", end="")


        # निर्गच्छ = exit
        elif आदेश == "निर्गच्छ":

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


def _open_file(path):
    """Open ``path`` with the platform opener — no shell involved."""
    if not os.path.isfile(path):
        print("संचिका नहीं मिली:", path)
        return False

    opener = None
    for candidate in ("termux-open", "xdg-open", "open"):
        if shutil.which(candidate):
            opener = candidate
            break

    if opener is None:
        print("कोई opener उपलब्ध नहीं (termux-open/xdg-open/open)")
        return False

    try:
        subprocess.run([opener, path], check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("खोलना विफल:", exc)
        return False
    return True
