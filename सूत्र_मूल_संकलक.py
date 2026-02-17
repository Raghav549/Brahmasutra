# 🕉️ सूत्र मूल यन्त्र संकलक


class मूलसंकलक:


    def __init__(self):

        self.bytecode = []

        print("🕉️ सूत्र मूल संकलक सक्रिय")


    def संकलन(self, स्रोत, लक्ष्य):

        print(f"संकलन प्रारम्भ: {स्रोत}")


        with open(स्रोत, "r", encoding="utf-8") as file:

            पंक्तियाँ = file.readlines()


        for पंक्ति in पंक्तियाँ:

            आदेश = पंक्ति.strip()

            कोड = self.अनुवाद(आदेश)

            if कोड:

                self.bytecode.append(कोड)


        with open(लक्ष्य, "wb") as file:

            for कोड in self.bytecode:

                file.write(कोड.to_bytes(4, "little"))


        print(f"संकलन पूर्ण → {लक्ष्य}")


    def अनुवाद(self, आदेश):

        भाग = आदेश.split()

        if not भाग:

            return None


        if भाग[0] == "संकल्प":

            return 1


        elif भाग[0] == "योग":

            return 2


        elif भाग[0] == "दर्शय":

            return 3


        elif भाग[0] == "निर्गम":

            return 0


        else:

            return 255
