class सूत्रPackageManager:

    def __init__(self):

        self.packages = {}

        print("सूत्र Package Manager आरम्भ")

    def स्थापित(self, नाम):

        self.packages[नाम] = "स्थापित"

        print(f"स्थापना सफल: {नाम}")

    def हटाएँ(self, नाम):

        if नाम in self.packages:

            del self.packages[नाम]

            print(f"हटाया गया: {नाम}")

        else:

            print("अनुप्रयोग न प्राप्त")

    def सूची(self):

        print("\nस्थापित Packages:")

        for नाम in self.packages:

            print(नाम)

    def अस्ति(self, नाम):

        return नाम in self.packages
