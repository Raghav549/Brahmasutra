"""बाइनरी निर्माता का लघु परीक्षण।

रेजिस्टर अ/ब/स/द को 0..3 के रूप में लिखा जाता है, क्योंकि bytearray में
केवल 0-255 मान संग्रहीत हो सकते हैं (देवनागरी अक्षर का ord() 2304+ है)।
"""

REGISTERS = {"अ": 0, "ब": 1, "स": 2, "द": 3}


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global data, f

    data = bytearray()

    # LOAD अ 10
    data.append(1)
    data.append(REGISTERS["अ"])
    data += (10).to_bytes(4, "big")

    # LOAD ब 20
    data.append(1)
    data.append(REGISTERS["ब"])
    data += (20).to_bytes(4, "big")

    # ADD अ ब
    data.append(2)
    data.append(REGISTERS["अ"])
    data.append(REGISTERS["ब"])

    # SHOW अ
    data.append(3)
    data.append(REGISTERS["अ"])

    # END
    data.append(4)

    with open("test.सूत्रबिन", "wb") as f:
        f.write(data)

    print("Binary created")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
