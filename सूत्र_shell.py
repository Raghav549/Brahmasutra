# =========================================
# सूत्र तंत्र — संस्कृत Shell
# =========================================



# स्मृति (Memory)
स्मृति = {}


# गणना प्रणाली

def योग(a, b):
    return a + b

def गुण(a, b):
    return a * b

def घट(a, b):
    return a - b

def भाग(a, b):
    return a / b


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global a, b, आदेश, नाम, परिणाम, मान, यदि
    print("🕉️ सूत्र तंत्र Shell सक्रिय")
    print("लिखत: सहायता  (सहायता हेतु)")
    print("लिखत: निर्गम  (बाहर जाने हेतु)")



    # मुख्य लूप

    while True:

        आदेश = input("सूत्र >>> ")

        यदि = आदेश.split()

        if len(यदि) == 0:
            continue


        # निर्गम

        if यदि[0] == "निर्गम":

            print("सूत्र Shell समाप्त")
            break


        # सहायता

        elif यदि[0] == "सहायता":

            print("उपलब्ध आदेश:")
            print("संकल्प नाम मान")
            print("दर्शय नाम")
            print("योग नाम१ नाम२")
            print("गुण नाम१ नाम२")
            print("घट नाम१ नाम२")
            print("भाग नाम१ नाम२")
            print("निर्गम")


        # Variable create

        elif यदि[0] == "संकल्प":

            नाम = यदि[1]
            मान = float(यदि[2])

            स्मृति[नाम] = मान

            print("संग्रहीत:", नाम, "=", मान)



        # Display

        elif यदि[0] == "दर्शय":

            नाम = यदि[1]

            if नाम in स्मृति:

                print("मान:", स्मृति[नाम])

            else:

                print("त्रुटि: अस्तित्व नहीं")



        # योग

        elif यदि[0] == "योग":

            a = स्मृति[यदि[1]]
            b = स्मृति[यदि[2]]

            परिणाम = योग(a, b)

            print("परिणाम:", परिणाम)



        # गुण

        elif यदि[0] == "गुण":

            a = स्मृति[यदि[1]]
            b = स्मृति[यदि[2]]

            परिणाम = गुण(a, b)

            print("परिणाम:", परिणाम)



        # घट

        elif यदि[0] == "घट":

            a = स्मृति[यदि[1]]
            b = स्मृति[यदि[2]]

            परिणाम = घट(a, b)

            print("परिणाम:", परिणाम)



        # भाग

        elif यदि[0] == "भाग":

            a = स्मृति[यदि[1]]
            b = स्मृति[यदि[2]]

            परिणाम = भाग(a, b)

            print("परिणाम:", परिणाम)



        else:

            print("त्रुटि: अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
