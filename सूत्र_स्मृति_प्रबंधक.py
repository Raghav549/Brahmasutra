# 🕉️ सूत्र स्मृति प्रबंधक


class स्मृति_प्रबंधक:


    def __init__(self):

        self.स्मृति = {}

        print("🕉️ स्मृति प्रबंधक निर्मित")


    def आवंटन(self, नाम, मान):

        self.स्मृति[नाम] = मान

        print(f"स्मृति आवंटित: {नाम} = {मान}")


    def पठन(self, नाम):

        if नाम in self.स्मृति:

            return self.स्मृति[नाम]

        else:

            print("त्रुटि: स्मृति नहीं मिला")

            return None


    def स्थिति(self):

        print("स्मृति स्थिति:")

        for नाम in self.स्मृति:

            print(f"{नाम} = {self.स्मृति[नाम]}")


# global instance

प्रबंधक = स्मृति_प्रबंधक()


def प्रारम्भ():

    print("🕉️ स्मृति तंत्र सक्रिय")
