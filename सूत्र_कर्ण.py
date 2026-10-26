# =========================================
# सूत्र तंत्र — संचालन तंत्र कर्ण (Kernel)
# =========================================



# प्रक्रिया सूची
प्रक्रिया_सूची = {}

# स्मृति
स्मृति = {}

# PID counter
अगला_PID = 1


def प्रक्रिया_निर्माण(नाम):

    global अगला_PID

    PID = अगला_PID

    प्रक्रिया_सूची[PID] = {

        "नाम": नाम,
        "स्थिति": "सक्रिय"

    }

    अगला_PID += 1

    print("प्रक्रिया निर्मित:", नाम, "PID:", PID)


def प्रक्रिया_समाप्त(PID):

    if PID in प्रक्रिया_सूची:

        प्रक्रिया_सूची[PID]["स्थिति"] = "समाप्त"

        print("प्रक्रिया समाप्त:", PID)

    else:

        print("प्रक्रिया नहीं मिली")


def प्रक्रिया_दर्शय():

    print("प्रक्रिया सूची:")

    for PID in प्रक्रिया_सूची:

        print(

            PID,
            प्रक्रिया_सूची[PID]["नाम"],
            प्रक्रिया_सूची[PID]["स्थिति"]

        )


def स्मृति_आवंटन(नाम, मान):

    स्मृति[नाम] = मान

    print("स्मृति आवंटित:", नाम)


def स्मृति_दर्शय():

    print("स्मृति स्थिति:")

    for नाम in स्मृति:

        print(नाम, "=", स्मृति[नाम])


सक्रिय = True


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आदेश, भाग
    print("🕉️ सूत्र संचालन तंत्र कर्ण सक्रिय")

    while सक्रिय:

        आदेश = input("कर्ण >>> ")

        भाग = आदेश.split()

        if len(भाग) == 0:
            continue


        if भाग[0] == "निर्गम":

            print("कर्ण बन्द")

            break


        elif भाग[0] == "सहायता":

            print("आदेश:")
            print("निर्माण नाम")
            print("समाप्त PID")
            print("प्रक्रिया")
            print("स्मृति नाम मान")
            print("स्मृति-दर्शय")
            print("निर्गम")


        elif भाग[0] == "निर्माण":

            प्रक्रिया_निर्माण(भाग[1])


        elif भाग[0] == "समाप्त":

            प्रक्रिया_समाप्त(int(भाग[1]))


        elif भाग[0] == "प्रक्रिया":

            प्रक्रिया_दर्शय()


        elif भाग[0] == "स्मृति":

            स्मृति_आवंटन(भाग[1], भाग[2])


        elif भाग[0] == "स्मृति-दर्शय":

            स्मृति_दर्शय()


        else:

            print("अज्ञात आदेश")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
