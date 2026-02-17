# 🕉️ सूत्र यन्त्र तंत्र


class यन्त्र:


    def __init__(self, नाम):

        self.नाम = नाम

        self.स्थिति = "बन्द"


    def चालू(self):

        self.स्थिति = "सक्रिय"

        print(f"{self.नाम} सक्रिय")


    def बन्द(self):

        self.स्थिति = "बन्द"

        print(f"{self.नाम} बन्द")



class यन्त्र_प्रबंधक:


    def __init__(self):

        self.यन्त्र = {}

        print("🕉️ यन्त्र प्रबंधक निर्मित")


    def पंजीकरण(self, नाम):

        y = यन्त्र(नाम)

        self.यन्त्र[नाम] = y

        print(f"यन्त्र पंजीकृत: {नाम}")

        return y


    def चालू(self, नाम):

        if नाम in self.यन्त्र:

            self.यन्त्र[नाम].चालू()


    def बन्द(self, नाम):

        if नाम in self.यन्त्र:

            self.यन्त्र[नाम].बन्द()


    def सूची(self):

        print("यन्त्र सूची:")

        for नाम in self.यन्त्र:

            print(नाम)



# global instance

प्रबंधक = यन्त्र_प्रबंधक()


def प्रारम्भ():

    print("🕉️ यन्त्र तंत्र सक्रिय")

    प्रबंधक.पंजीकरण("CPU")

    प्रबंधक.पंजीकरण("Memory")

    प्रबंधक.पंजीकरण("Storage")
