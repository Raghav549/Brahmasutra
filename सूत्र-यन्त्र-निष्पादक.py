# =========================================
# सूत्र स्वदेशी यन्त्र निष्पादक
# =========================================

import struct


# registers
रजिस्टर = {

    1: 0,
    2: 0,
    3: 0,
    4: 0

}


नाम_मानचित्र = {

    1: "अ",
    2: "ब",
    3: "स",
    4: "द"

}


def दर्शय(reg):

    print(नाम_मानचित्र[reg], "=", रजिस्टर[reg])


def निष्पादन(संचिका):

    with open(संचिका, "rb") as f:

        while True:

            op_byte = f.read(1)

            if not op_byte:
                break


            op = struct.unpack("B", op_byte)[0]


            if op == 1:   # स्थापय

                reg = struct.unpack("B", f.read(1))[0]

                val = struct.unpack("I", f.read(4))[0]

                रजिस्टर[reg] = val

                print("स्थापित:", नाम_मानचित्र[reg], val)


            elif op == 2:  # योग

                reg1 = struct.unpack("B", f.read(1))[0]

                reg2 = struct.unpack("B", f.read(1))[0]

                रजिस्टर[reg1] += रजिस्टर[reg2]

                print("योग पूर्ण")


            elif op == 3:  # घटा

                reg1 = struct.unpack("B", f.read(1))[0]

                reg2 = struct.unpack("B", f.read(1))[0]

                रजिस्टर[reg1] -= रजिस्टर[reg2]

                print("घटाव पूर्ण")


            elif op == 4:  # गुण

                reg1 = struct.unpack("B", f.read(1))[0]

                reg2 = struct.unpack("B", f.read(1))[0]

                रजिस्टर[reg1] *= रजिस्टर[reg2]

                print("गुणन पूर्ण")


            elif op == 5:  # दर्शय

                reg = struct.unpack("B", f.read(1))[0]

                दर्शय(reg)


            else:

                print("अज्ञात opcode")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global नाम


    print("🕉️ सूत्र यन्त्र निष्पादक सक्रिय")


    नाम = input("यन्त्र संचिका नाम: ")

    print("निष्पादन प्रारम्भ")

    निष्पादन(नाम)

    print("निष्पादन समाप्त")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
