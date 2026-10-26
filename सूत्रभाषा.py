# सूत्र तंत्र — सूत्रभाषा v1.0
# Production Sanskrit Programming Language




# memory
चर = {}



# evaluate value
def मान_प्राप्त(शब्द):

    if शब्द.isdigit():

        return int(शब्द)

    elif शब्द in चर:

        return चर[शब्द]

    else:

        return 0



# execute line
def पंक्ति_चलाओ(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:

        return



    # variable assign
    if शब्द[0] == "संकल्प":

        नाम = शब्द[1]

        मान = मान_प्राप्त(शब्द[2])

        चर[नाम] = मान

        print("चर:", नाम, "=", मान)



    # print
    elif शब्द[0] == "दर्शय":

        मान = मान_प्राप्त(शब्द[1])

        print("दर्शय:", मान)



    # addition
    elif शब्द[0] == "योग":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        परिणाम = अ + ब

        print("योग:", परिणाम)



    # subtraction
    elif शब्द[0] == "वियोग":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        परिणाम = अ - ब

        print("वियोग:", परिणाम)



    # multiplication
    elif शब्द[0] == "गुण":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        परिणाम = अ * ब

        print("गुण:", परिणाम)



    # division
    elif शब्द[0] == "भाग":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        if ब != 0:

            परिणाम = अ // ब

            print("भाग:", परिणाम)

        else:

            print("त्रुटि: शून्य से भाग")



    else:

        print("अज्ञात आदेश:", पंक्ति)



# interactive shell
def संवाद():

    print("सूत्रभाषा संवाद मोड")

    while True:

        पंक्ति = input("सूत्रभाषा > ")

        if पंक्ति == "निर्गम":

            break

        पंक्ति_चलाओ(पंक्ति)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्रभाषा v1.0 आरम्भ")



    # start
    संवाद()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
