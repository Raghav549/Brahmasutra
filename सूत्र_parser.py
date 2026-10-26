# 🕉️ सूत्र Parser

class Parser:

    def __init__(self):
        print("🕉️ सूत्र Parser सक्रिय")

    def parse_file(self, filename):

        ast = []

        with open(filename,"r",encoding="utf-8") as f:

            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            parts = line.split()

            instruction = {}

            instruction["op"] = parts[0]

            if len(parts) > 1:
                instruction["arg1"] = parts[1]

            if len(parts) > 2:
                instruction["arg2"] = parts[2]

            ast.append(instruction)

        return ast


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र Parser तैयार")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
