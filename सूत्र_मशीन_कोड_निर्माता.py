# 🕉️ सूत्र मशीन कोड निर्माता

class मशीनकोडनिर्माता:

    def __init__(self):
        self.opcodes = {
            "संकल्प": "0001",
            "योग": "0010",
            "दर्शय": "0011",
            "निर्गम": "1111"
        }

    def निर्मित(self, bytecode):

        machine_code = []

        for instruction in bytecode:

            op = instruction["op"]

            if op in self.opcodes:

                code = self.opcodes[op]

                if "arg1" in instruction:
                    code += format(hash(instruction["arg1"]) & 0xFFFF, '016b')

                if "arg2" in instruction:
                    code += format(hash(instruction["arg2"]) & 0xFFFF, '016b')

                machine_code.append(code)

        return machine_code


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():


    print("🕉️ सूत्र मशीन कोड निर्माता सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
