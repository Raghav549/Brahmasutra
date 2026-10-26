# सूत्र तंत्र — पूर्ण सूत्रभाषा v2
# Fixed Panini-integrated Sanskrit Programming Language




# memory
चर = {}



# validate word
def शब्द_मान्य(शब्द):

    for अक्षर in शब्द:

        if अक्षर in वर्ण:
            continue

        elif अक्षर.isdigit():
            continue

        else:
            return False

    return True



# get value
def मान_प्राप्त(शब्द):

    if शब्द.isdigit():

        return int(शब्द)

    elif शब्द in चर:

        return चर[शब्द]

    else:

        print("त्रुटि: अज्ञात चर", शब्द)

        return 0



# execute line
def पंक्ति_चलाओ(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:

        return


    आदेश = शब्द[0]


    # validate words
    for श in शब्द:

        if not शब्द_मान्य(श):

            print("त्रुटि: अमान्य शब्द", श)

            return


    # संकल्प
    if आदेश == "संकल्प":

        नाम = शब्द[1]

        मान = मान_प्राप्त(शब्द[2])

        चर[नाम] = मान

        print("निर्मित:", नाम, "=", मान)


    # दर्शय
    elif आदेश == "दर्शय":

        मान = मान_प्राप्त(शब्द[1])

        print("मान:", मान)


    # योग
    elif आदेश == "योग":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        print("योग:", अ + ब)


    # गुण
    elif आदेश == "गुण":

        अ = मान_प्राप्त(शब्द[1])

        ब = मान_प्राप्त(शब्द[2])

        print("गुण:", अ * ब)


    else:

        print("त्रुटि: अज्ञात आदेश", आदेश)



# shell
def संवाद():

    print("सूत्रभाषा संवाद सक्रिय")

    while True:

        पंक्ति = input("सूत्र >>> ")

        if पंक्ति == "निर्गम":

            break

        पंक्ति_चलाओ(पंक्ति)


वर्ण = set(
"अआइईउऊऋएऐओऔ"
"कखगघङचछजझञ"
"टठडढणतथदधन"
"पफबभमयरलव"
"शषसह"
"ािीुूृेैोौंः्"
)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("पूर्ण सूत्रभाषा v2 आरम्भ")



    # FULL Sanskrit character set



    # start
    संवाद()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
