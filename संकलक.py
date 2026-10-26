# सूत्र तंत्र — संस्कृत संकलक
# Sanskrit Compiler




# opcode mapping
आदेशसङ्ख्या = {

    "संकल्प": 1,
    "दर्शय": 2,
    "योग": 3

}



# compile one line
def पंक्ति_संकलन(पंक्ति):

    शब्द = पंक्ति.strip().split()

    if len(शब्द) == 0:

        return None

    आदेश = शब्द[0]

    if आदेश not in आदेशसङ्ख्या:

        print("त्रुटि: अज्ञात आदेश", आदेश)

        return None

    opcode = आदेशसङ्ख्या[आदेश]

    operands = शब्द[1:]

    return (opcode, operands)



# compile file
def कार्यक्रम_संकलन(इनपुट, आउटपुट):

    bytecode = []

    with open(इनपुट, "r", encoding="utf-8") as f:

        for पंक्ति in f:

            compiled = पंक्ति_संकलन(पंक्ति)

            if compiled:

                bytecode.append(compiled)


    with open(आउटपुट, "w", encoding="utf-8") as f:

        for opcode, operands in bytecode:

            f.write(str(opcode) + " " + " ".join(operands) + "\n")


    print("संकलन पूर्ण:", आउटपुट)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global f
    print("संस्कृत संकलक आरम्भ")
    print("उदाहरण संकलन")

    with open("परीक्षण.sutra", "w", encoding="utf-8") as f:

        f.write("संकल्प x 5\n")
        f.write("दर्शय x\n")


    कार्यक्रम_संकलन("परीक्षण.sutra", "परीक्षण.bytecode")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
