# सूत्र तंत्र — CPU Core




रजिस्टर = {

    "अ": 0,
    "ब": 0,
    "स": 0,
    "द": 0

}



def चलाओ(निर्देश, op1=None, op2=None):

    if निर्देश == "लोड":

        रजिस्टर[op1] = op2


    elif निर्देश == "योग":

        रजिस्टर[op1] += रजिस्टर[op2]


    elif निर्देश == "गुण":

        रजिस्टर[op1] *= रजिस्टर[op2]


    elif निर्देश == "दर्शय":

        print("मान:", रजिस्टर[op1])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र CPU Core सक्रिय")



    चलाओ("लोड", "अ", 10)
    चलाओ("लोड", "ब", 5)
    चलाओ("योग", "अ", "ब")
    चलाओ("दर्शय", "अ")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
