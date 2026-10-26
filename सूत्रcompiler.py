# सूत्र तंत्र — Compiler
# संस्कृत source → bytecode


import json


BYTECODE_FILE = "program.sbc"


def compile_line(पंक्ति):

    पंक्ति = पंक्ति.strip()

    if पंक्ति.startswith("संकल्प"):

        भाग = पंक्ति.replace("संकल्प", "").strip()

        नाम, मान = भाग.split("=")

        return {
            "opcode": "SET",
            "name": नाम.strip(),
            "value": मान.strip()
        }

    elif पंक्ति.startswith("मुद्रय"):

        नाम = पंक्ति.replace("मुद्रय", "").strip()

        return {
            "opcode": "PRINT",
            "name": नाम
        }

    return None


def compile_file(source, output):

    bytecode = []

    with open(source, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            instr = compile_line(पंक्ति)

            if instr:
                bytecode.append(instr)

    with open(output, "w", encoding="utf-8") as f:

        json.dump(bytecode, f, ensure_ascii=False, indent=4)

    print("संकलन सफल:", output)


def परीक्षण():

    print("सूत्र Compiler सक्रिय")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    परीक्षण()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
