# सूत्र तंत्र — Sanskrit Shell




# memory
चर = {}



# process list
प्रक्रिया = []



# commands
def आदेश_चलाओ(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:
        return


    आदेश = शब्द[0]


    # exit
    if आदेश == "निर्गम":

        print("Shell समाप्त")

        exit()


    # create variable
    elif आदेश == "संकल्प":

        नाम = शब्द[1]

        मान = शब्द[2]

        चर[नाम] = मान

        print("चर निर्मित:", नाम, "=", मान)


    # show variable
    elif आदेश == "दर्शय":

        नाम = शब्द[1]

        if नाम in चर:

            print("मान:", चर[नाम])

        else:

            print("चर नहीं मिला")


    # create process
    elif आदेश == "प्रक्रिया":

        नाम = शब्द[1]

        प्रक्रिया.append(नाम)

        print("प्रक्रिया आरम्भ:", नाम)


    # show processes
    elif आदेश == "सूची":

        print("प्रक्रिया सूची:")

        for p in प्रक्रिया:

            print(p)


    else:

        print("अज्ञात आदेश")



# shell loop
def shell():

    while True:

        cmd = input("सूत्र> ")

        आदेश_चलाओ(cmd)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Shell आरम्भ")
    shell()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
