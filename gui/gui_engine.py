# सूत्र GUI Engine

class सूत्रGUI:

    def __init__(self):
        self.शीर्षक = ""
        self.घटकाः = []

    def शीर्षक_निर्धारण(self, नाम):
        self.शीर्षक = नाम

    def बटन_निर्माण(self, नाम, क्रिया):
        self.घटकाः.append(("बटन", नाम, क्रिया))

    def पाठ_निर्माण(self, पाठ):
        self.घटकाः.append(("पाठ", पाठ))

    def प्रदर्शय(self):
        print("========")
        print("सूत्र GUI")
        print("शीर्षक:", self.शीर्षक)
        print("========")

        for घटक in self.घटकाः:

            if घटक[0] == "पाठ":
                print("पाठ:", घटक[1])

            elif घटक[0] == "बटन":
                print("बटन:", घटक[1])

        print("========")

    def चल(self):
        self.प्रदर्शय()

        while True:

            आदेश = input("चयन करें: ")

            if आदेश == "निर्गच्छ":
                print("GUI समाप्त")
                break

            for घटक in self.घटकाः:

                if घटक[0] == "बटन" and घटक[1] == आदेश:
                    घटक[2]()
