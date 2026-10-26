# =========================================
# सूत्र तंत्र — बाइटकोड निर्माता
# =========================================



# आदेश से बाइटकोड mapping

कोड = {

    "स्थापय": "01",
    "योग": "02",
    "घटा": "03",
    "गुण": "04",
    "स्मृति": "05",
    "लोड": "06",
    "दर्शय": "07"

}


def बाइटकोड_निर्माण(पंक्ति):

    भाग = पंक्ति.split()

    आदेश = भाग[0]

    यदि = कोड.get(आदेश, "00")

    return यदि + " " + " ".join(भाग[1:])


def संचिका_पढ़ो(नाम):

    with open(नाम, "r", encoding="utf-8") as f:

        return f.readlines()


def संचिका_लिखो(नाम, पंक्तियाँ):

    with open(नाम, "w", encoding="utf-8") as f:

        for पंक्ति in पंक्तियाँ:

            f.write(पंक्ति + "\n")

बाइटसूची = []


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global आउटपुट, इनपुट, पंक्ति, पंक्तियाँ, यदि
    print("🕉️ सूत्र बाइटकोड निर्माता सक्रिय")


    # input program
    इनपुट = input("प्रोग्राम संचिका नाम: ")

    # output bytecode file
    आउटपुट = input("बाइटकोड संचिका नाम: ")


    पंक्तियाँ = संचिका_पढ़ो(इनपुट)

    for पंक्ति in पंक्तियाँ:

        पंक्ति = पंक्ति.strip()

        यदि = बाइटकोड_निर्माण(पंक्ति)

        बाइटसूची.append(यदि)


    संचिका_लिखो(आउटपुट, बाइटसूची)

    print("बाइटकोड निर्मित:", आउटपुट)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
