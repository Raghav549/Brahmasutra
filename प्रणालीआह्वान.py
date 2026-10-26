# सूत्र तंत्र — प्रणाली आह्वान प्रणाली
# Sanskrit System Call Interface


# system call registry
आह्वानसूची = {}



# register system call
def आह्वान_पंजीकरण(नाम, कार्य):

    आह्वानसूची[नाम] = कार्य

    print("आह्वान पंजीकृत:", नाम)



# execute system call
def आह्वान_चलाओ(नाम, पैरामीटर=None):

    if नाम not in आह्वानसूची:

        print("त्रुटि: आह्वान नहीं मिला")

        return

    कार्य = आह्वानसूची[नाम]

    if पैरामीटर == None:

        return कार्य()

    else:

        return कार्य(पैरामीटर)



# example system calls

def नमस्ते():

    print("नमस्ते सूत्र तंत्र")



def जोड़(मान):

    परिणाम = मान + मान

    print("परिणाम:", परिणाम)

    return परिणाम


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("प्रणाली आह्वान प्रणाली आरम्भ")



    # register calls
    आह्वान_पंजीकरण("नमस्ते", नमस्ते)

    आह्वान_पंजीकरण("जोड़", जोड़)



    # execute calls
    आह्वान_चलाओ("नमस्ते")

    आह्वान_चलाओ("जोड़", 5)



    print("प्रणाली आह्वान सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
