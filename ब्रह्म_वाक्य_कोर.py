# 🕉️ ब्रह्म वाक्य कोर VERSION 2


class ब्रह्मवाक्यकोर:

    def __init__(self):

        self.मान्य_आदेश = [
            "स्थापित",
            "दर्शय",
            "योग"
        ]

    def विश्लेषण(self, वाक्य):

        वाक्य = वाक्य.strip()

        if वाक्य == "":
            return {
                "मान्य": False,
                "शब्द": []
            }

        शब्द = वाक्य.split()

        if शब्द[0] in self.मान्य_आदेश:

            return {
                "मान्य": True,
                "शब्द": शब्द
            }

        return {
            "मान्य": False,
            "शब्द": शब्द
        }


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म वाक्य कोर सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
