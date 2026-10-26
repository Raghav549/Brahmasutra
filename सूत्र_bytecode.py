# 🕉️ सूत्र Bytecode Generator

class BytecodeGenerator:

    def __init__(self):

        print("🕉️ सूत्र Bytecode Generator सक्रिय")

    def generate(self, ast):

        bytecode = []

        for instruction in ast:

            code = {}

            code["op"] = instruction["op"]

            if "arg1" in instruction:
                code["arg1"] = instruction["arg1"]

            if "arg2" in instruction:
                code["arg2"] = instruction["arg2"]

            bytecode.append(code)

        return bytecode


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र Bytecode प्रणाली तैयार")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
