# सूत्र तंत्र — पाणिनि व्याकरण इंजन
# Panini Grammar Engine




# धातु सूची (basic roots)
धातु = {

    "गम्": "जाना",
    "भू": "होना",
    "कृ": "करना",
    "दृश्": "देखना"

}



# शब्द validate
def शब्द_मान्य(शब्द):

    for अक्षर in शब्द:

        if अक्षर not in वर्ण:

            return False

    return True



# धातु पहचान
def धातु_पहचान(शब्द):

    for मूल in धातु:

        if शब्द.startswith(मूल):

            return मूल

    return None



# व्याकरण विश्लेषण
def विश्लेषण(वाक्य):

    शब्दसूची = वाक्य.split()

    print("विश्लेषण:")

    for शब्द in शब्दसूची:

        if शब्द_मान्य(शब्द):

            print("मान्य शब्द:", शब्द)

        else:

            print("अमान्य शब्द:", शब्द)


        मूल = धातु_पहचान(शब्द)

        if मूल:

            print("धातु मिली:", मूल, "अर्थ:", धातु[मूल])


वर्ण = set("अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global वाक्य
    print("पाणिनि इंजन आरम्भ")



    # वर्ण सूची



    # test
    while True:

        वाक्य = input("सूत्र व्याकरण > ")

        if वाक्य == "निर्गम":

            break

        विश्लेषण(वाक्य)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
