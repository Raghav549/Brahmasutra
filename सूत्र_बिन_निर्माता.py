# 🕉️ सूत्र Native Binary निर्माता


MAGIC = b"SUTRA"


class बिननिर्माता:


    def निर्माण(self, स्रोत, लक्ष्य):

        print("Binary निर्माण प्रारम्भ:", स्रोत)


        with open(स्रोत, "rb") as file:

            मशीन = file.read()


        with open(लक्ष्य, "wb") as file:

            # Header
            file.write(MAGIC)

            # Size
            file.write(len(मशीन).to_bytes(4, "little"))

            # Code
            file.write(मशीन)


        print("Binary निर्माण पूर्ण:", लक्ष्य)
