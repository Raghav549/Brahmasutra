# 🕉️ ब्रह्म निष्पादन कोर


class ब्रह्मनिष्पादनकोर:

    def __init__(self):

        print("🕉️ ब्रह्म वाक्य कोर सक्रिय")

        self.चर = {}


    def आदेश_चलाओ(self, line):

        line = line.strip()

        if not line:
            return


        भाग = line.split()


        आदेश = भाग[0]


        if आदेश == "स्थापित":

            नाम = भाग[1]
            मान = int(भाग[2])

            self.चर[नाम] = मान

            print(f"स्थापित: {नाम} = {मान}")


        elif आदेश == "योग":

            नाम = भाग[1]
            अन्य = भाग[2]

            self.चर[नाम] = self.चर.get(नाम, 0) + self.चर.get(अन्य, 0)

            print(f"योग: {नाम} = {self.चर[नाम]}")


        elif आदेश == "दर्शय":

            नाम = भाग[1]

            मान = self.चर.get(नाम, 0)

            print(f"{नाम} = {मान}")


        else:

            print("त्रुटि: अमान्य आदेश", आदेश)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म निष्पादन कोर सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
