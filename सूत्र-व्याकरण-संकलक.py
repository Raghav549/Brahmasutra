# सूत्र तंत्र — Panini Grammar Compiler




# memory
चर = {}



# function registry
कर्म_पंजी = {}



# execute block
def खण्ड_चलाओ(पंक्तियाँ):

    i = 0

    while i < len(पंक्तियाँ):

        पंक्ति = पंक्तियाँ[i].strip()

        शब्द = पंक्ति.split()

        if len(शब्द) == 0:

            i += 1
            continue


        आदेश = शब्द[0]


        # संकल्प
        if आदेश == "संकल्प":

            नाम = शब्द[1]

            मान = int(शब्द[2])

            चर[नाम] = मान

            print("चर:", नाम, "=", मान)


        # दर्शय
        elif आदेश == "दर्शय":

            नाम = शब्द[1]

            print("मान:", चर.get(नाम, 0))


        # योग
        elif आदेश == "योग":

            अ = चर.get(शब्द[1], 0)

            ब = char.get(शब्द[2], 0)

            print("योग:", अ + ब)


        # यदि
        elif आदेश == "यदि":

            var = शब्द[1]

            value = int(शब्द[2])

            if चर.get(var, 0) == value:

                print("शर्त सत्य")

            else:

                print("शर्त असत्य")


        i += 1



# run program
def कार्यक्रम_चलाओ(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()

    खण्ड_चलाओ(lines)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Panini Compiler आरम्भ")
    कार्यक्रम_चलाओ("test.panini")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
