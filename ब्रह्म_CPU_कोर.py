# 🕉️ ब्रह्म CPU कोर
# VERSION 13


from ब्रह्म_स्मृति_प्रबंधक_कोर import ब्रह्मस्मृतिप्रबंधककोर


class ब्रह्मCPUकोर:

    def __init__(self):

        self.स्मृति = ब्रह्मस्मृतिप्रबंधककोर()

        self.रजिस्टर = {}

        print("CPU तैयार")


    def स्थापित(self, नाम, मान):

        address = self.स्मृति.आवंटन(मान)

        self.रजिस्टर[नाम] = address

        print(f"रजिस्टर स्थापित: {नाम} → {address}")


    def पढ़ो(self, नाम):

        if नाम in self.रजिस्टर:

            address = self.रजिस्टर[नाम]

            return self.स्मृति.पढ़ो(address)

        else:

            print("त्रुटि: रजिस्टर नहीं मिला")

            return None


    def लिखो(self, नाम, मान):

        if नाम in self.रजिस्टर:

            address = self.रजिस्टर[नाम]

            self.स्मृति.लिखो(address, मान)

        else:

            print("त्रुटि: रजिस्टर नहीं मिला")


    def योग(self, लक्ष्य, स्रोत):

        v1 = self.पढ़ो(लक्ष्य)

        v2 = self.पढ़ो(स्रोत)

        if v1 is not None and v2 is not None:

            result = v1 + v2

            self.लिखो(लक्ष्य, result)

            print(f"योग: {लक्ष्य} = {result}")


    def घटाव(self, लक्ष्य, स्रोत):

        v1 = self.पढ़ो(लक्ष्य)

        v2 = self.पढ़ो(स्रोत)

        if v1 is not None and v2 is not None:

            result = v1 - v2

            self.लिखो(लक्ष्य, result)

            print(f"घटाव: {लक्ष्य} = {result}")


    def गुणा(self, लक्ष्य, स्रोत):

        v1 = self.पढ़ो(लक्ष्य)

        v2 = self.पढ़ो(स्रोत)

        if v1 is not None and v2 is not None:

            result = v1 * v2

            self.लिखो(लक्ष्य, result)

            print(f"गुणा: {लक्ष्य} = {result}")


    def दर्शय(self, नाम):

        value = self.पढ़ो(नाम)

        print(f"{नाम} = {value}")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म CPU कोर सक्रिय")
    cpu = ब्रह्मCPUकोर()

    cpu.स्थापित("अ", 10)

    cpu.स्थापित("ब", 20)

    cpu.योग("अ", "ब")

    cpu.दर्शय("अ")

    cpu.घटाव("अ", "ब")

    cpu.दर्शय("अ")

    cpu.गुणा("अ", "ब")

    cpu.दर्शय("अ")


if __name__ == "__main__":
    _main()
