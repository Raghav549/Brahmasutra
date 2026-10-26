# =========================================
# सूत्र तंत्र — सूत्र संकलक
# =========================================



# opcode mapping

निर्देश_कोड = {

    "स्थापय": "INST_SET",
    "योग": "INST_ADD",
    "घटा": "INST_SUB",
    "गुण": "INST_MUL",
    "स्मृति": "INST_STORE",
    "लोड": "INST_LOAD",
    "दर्शय": "INST_PRINT"

}


def संचिका_पढ़ो(नाम):

    with open(नाम, "r", encoding="utf-8") as f:

        return f.readlines()


def संचिका_लिखो(नाम, पंक्तियाँ):

    with open(नाम, "w", encoding="utf-8") as f:

        for पंक्ति in पंक्तियाँ:

            f.write(पंक्ति + "\n")


def संकलन(इनपुट):

    आउटपुट = []

    पंक्तियाँ = संचिका_पढ़ो(इनपुट)


    for पंक्ति in पंक्तियाँ:

        पंक्ति = पंक्ति.strip()

        भाग = पंक्ति.split()

        आदेश = भाग[0]


        कोड = निर्देश_कोड.get(आदेश, "UNKNOWN")

        नया = कोड + " " + " ".join(भाग[1:])

        आउटपुट.append(नया)


    return आउटपुट


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आउटपुट, इनपुट, परिणाम
    print("🕉️ सूत्र संकलक सक्रिय")


    इनपुट = input("सूत्र संचिका नाम: ")

    आउटपुट = input("संकलित संचिका नाम (.सूत्रक): ")


    परिणाम = संकलन(इनपुट)

    संचिका_लिखो(आउटपुट, परिणाम)


    print("संकलन पूर्ण:", आउटपुट)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
