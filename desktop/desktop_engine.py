from window.window_manager import सूत्रविंडोप्रबंधक

class सूत्रडेस्कटॉप:

    def __init__(self):

        self.wm = सूत्रविंडोप्रबंधक()

        self.अनुप्रयोग = {}

        print("सूत्र डेस्कटॉप आरम्भ")

    def अनुप्रयोग_पंजीकरण(self, नाम, कार्य):

        self.अनुप्रयोग[नाम] = कार्य

        print(f"अनुप्रयोग पंजीकृत: {नाम}")

    def अनुप्रयोग_चलाएँ(self, नाम):

        if नाम in self.अनुप्रयोग:

            विंडो = self.wm.विंडो_निर्माण(नाम)

            self.अनुप्रयोग[नाम](self.wm, विंडो)

            self.wm.प्रदर्शन()

        else:

            print("अनुप्रयोग न प्राप्त")

    def आरम्भ(self):

        print("\nडेस्कटॉप सक्रिय\n")

        while True:

            आदेश = input("सूत्र-डेस्कटॉप> ")

            if आदेश == "सूची":

                for app in self.अनुप्रयोग:

                    print(app)

            elif आदेश.startswith("चल"):

                नाम = आदेश.split(" ")[1]

                self.अनुप्रयोग_चलाएँ(नाम)

            elif आदेश == "निर्गम":

                print("डेस्कटॉप समाप्त")

                break

            else:

                print("अज्ञात आदेश")
