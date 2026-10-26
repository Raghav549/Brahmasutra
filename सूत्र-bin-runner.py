# सूत्र तंत्र — Machine Executor




# registers
reg = {
    "अ": 0,
    "ब": 0
}



# decode
decode = {
    "01": "लोड",
    "02": "योग",
    "03": "गुण",
    "04": "दर्शय"
}



def run(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    for line in lines:

        parts = line.strip().split()

        code = parts[0]


        cmd = decode[code]


        if cmd == "लोड":

            reg[parts[1]] = int(parts[2])

            print("लोड:", parts[1], reg[parts[1]])


        elif cmd == "योग":

            reg[parts[1]] += reg[parts[2]]

            print("योग:", reg[parts[1]])


        elif cmd == "गुण":

            reg[parts[1]] *= reg[parts[2]]

            print("गुण:", reg[parts[1]])


        elif cmd == "दर्शय":

            print("मान:", reg[parts[1]])


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Machine Runner आरम्भ")
    run("cpu.सूत्रbin")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
