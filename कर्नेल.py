# सूत्र तंत्र — मूल कर्नेल
# Sanskrit Native Kernel




# kernel state
स्थिति = "आरम्भ"



# modules registry
मॉड्यूल = {}



# register module
def मॉड्यूल_पंजीकरण(नाम, कार्य):

    मॉड्यूल[नाम] = कार्य

    print("मॉड्यूल पंजीकृत:", नाम)



# start module
def मॉड्यूल_आरम्भ(नाम):

    if नाम not in मॉड्यूल:

        print("त्रुटि: मॉड्यूल नहीं मिला")

        return

    print("मॉड्यूल आरम्भ:", नाम)

    मॉड्यूल[नाम]()



# kernel boot
def कर्नेल_प्रज्वलन():

    global स्थिति

    स्थिति = "सक्रिय"

    print("कर्नेल प्रज्वलित")

    for नाम in मॉड्यूल:

        मॉड्यूल_आरम्भ(नाम)



# kernel shutdown
def कर्नेल_समाप्त():

    global स्थिति

    स्थिति = "समाप्त"

    print("कर्नेल समाप्त")



# kernel status
def कर्नेल_स्थिति():

    print("कर्नेल स्थिति:", स्थिति)



# example modules

def स्मृति():

    print("स्मृति मॉड्यूल सक्रिय")



def प्रक्रिया():

    print("प्रक्रिया मॉड्यूल सक्रिय")



def सञ्चिका():

    print("सञ्चिका मॉड्यूल सक्रिय")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("मूल कर्नेल आरम्भ")



    # register modules
    मॉड्यूल_पंजीकरण("स्मृति", स्मृति)
    मॉड्यूल_पंजीकरण("प्रक्रिया", प्रक्रिया)
    मॉड्यूल_पंजीकरण("सञ्चिका", सञ्चिका)



    # boot kernel
    कर्नेल_स्थिति()

    कर्नेल_प्रज्वलन()

    कर्नेल_स्थिति()

    कर्नेल_समाप्त()

    कर्नेल_स्थिति()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
