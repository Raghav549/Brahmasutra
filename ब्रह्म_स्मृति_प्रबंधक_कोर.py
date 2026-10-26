# 🕉️ ब्रह्म स्मृति प्रबंधक कोर
# VERSION 12



class ब्रह्मस्मृतिखण्ड:

    def __init__(self, address, value):

        self.address = address
        self.value = value


class ब्रह्मस्मृतिप्रबंधककोर:

    def __init__(self):

        self.memory = {}

        self.next_address = 1000

        print("स्मृति प्रबंधक तैयार")


    def आवंटन(self, मान):

        address = self.next_address

        self.memory[address] = ब्रह्मस्मृतिखण्ड(address, मान)

        self.next_address += 1

        print(f"स्मृति आवंटित: {address} = {मान}")

        return address


    def पढ़ो(self, address):

        if address in self.memory:

            value = self.memory[address].value

            print(f"स्मृति पढ़ी: {address} = {value}")

            return value

        else:

            print("त्रुटि: स्मृति नहीं मिली")

            return None


    def लिखो(self, address, मान):

        if address in self.memory:

            self.memory[address].value = मान

            print(f"स्मृति अपडेट: {address} = {मान}")

        else:

            print("त्रुटि: स्मृति नहीं मिली")


    def मुक्त(self, address):

        if address in self.memory:

            del self.memory[address]

            print(f"स्मृति मुक्त: {address}")

        else:

            print("त्रुटि: स्मृति नहीं मिली")


    def सूची(self):

        print("स्मृति स्थिति:")

        for address in self.memory:

            value = self.memory[address].value

            print(f"{address} = {value}")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global addr1, addr2, memory
    print("🕉️ ब्रह्म स्मृति प्रबंधक कोर सक्रिय")
    memory = ब्रह्मस्मृतिप्रबंधककोर()

    addr1 = memory.आवंटन(10)

    addr2 = memory.आवंटन(20)

    memory.पढ़ो(addr1)

    memory.लिखो(addr1, 999)

    memory.पढ़ो(addr1)

    memory.सूची()

    memory.मुक्त(addr2)

    memory.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
