# सूत्र तंत्र — अनुप्रयोग ढाँचा
# Sanskrit Application Framework


# app registry
अनुप्रयोगसूची = {}

# active app
सक्रिय = None



# register app
def अनुप्रयोग_पंजीकरण(नाम, कार्य):

    अनुप्रयोगसूची[नाम] = कार्य

    print("अनुप्रयोग पंजीकृत:", नाम)



# run app
def अनुप्रयोग_चलाओ(नाम):

    global सक्रिय

    if नाम not in अनुप्रयोगसूची:

        print("त्रुटि: अनुप्रयोग नहीं मिला")

        return

    सक्रिय = नाम

    print("अनुप्रयोग चल रहा:", नाम)

    अनुप्रयोगसूची[नाम]()



# close app
def अनुप्रयोग_समाप्त():

    global सक्रिय

    if सक्रिय == None:

        print("कोई सक्रिय अनुप्रयोग नहीं")

        return

    print("अनुप्रयोग बंद:", सक्रिय)

    सक्रिय = None



# show apps
def अनुप्रयोग_सूची():

    print("उपलब्ध अनुप्रयोग:")

    for नाम in अनुप्रयोगसूची:

        print("-", नाम)



# example apps

def गणक():

    print("गणक अनुप्रयोग सक्रिय")

    परिणाम = 5 + 3

    print("परिणाम:", परिणाम)



def नमस्ते():

    print("नमस्ते अनुप्रयोग सक्रिय")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("अनुप्रयोग ढाँचा आरम्भ")



    # register example apps
    अनुप्रयोग_पंजीकरण("गणक", गणक)

    अनुप्रयोग_पंजीकरण("नमस्ते", नमस्ते)



    # test
    अनुप्रयोग_सूची()

    अनुप्रयोग_चलाओ("गणक")

    अनुप्रयोग_समाप्त()

    अनुप्रयोग_चलाओ("नमस्ते")

    अनुप्रयोग_समाप्त()



    print("अनुप्रयोग ढाँचा सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
