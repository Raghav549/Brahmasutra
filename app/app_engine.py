class सूत्रअनुप्रयोग:

    def __init__(self, नाम, कार्य):

        self.नाम = नाम

        self.कार्य = कार्य

class सूत्रAppFramework:

    def __init__(self):

        self.apps = {}

        print("सूत्र Application Framework आरम्भ")

    def पंजीकरण(self, app):

        self.apps[app.नाम] = app

        print(f"अनुप्रयोग स्थापित: {app.नाम}")

    def चलाएँ(self, नाम, wm):

        if नाम in self.apps:

            विंडो = wm.विंडो_निर्माण(नाम)

            self.apps[नाम].कार्य(wm, विंडो)

            wm.प्रदर्शन()

        else:

            print("अनुप्रयोग न प्राप्त")

    def सूची(self):

        print("\nस्थापित अनुप्रयोग:")

        for नाम in self.apps:

            print(नाम)
