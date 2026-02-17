from ब्रह्म_संस्कृत_निष्पादन_इंजन import ब्रह्मसंस्कृतनिष्पादनइंजन


class ब्रह्मसंस्कृतशेल:

    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत शेल प्रारंभ")
        print("लिखें 'बाहर' बंद करने के लिए\n")

        self.engine = ब्रह्मसंस्कृतनिष्पादनइंजन()


    def प्रारंभ(self):

        while True:

            try:

                command = input("सूत्र> ")

                if command.strip() == "बाहर":

                    print("🕉️ शेल बंद")
                    break

                result = self.engine.निष्पादित(command)

                print("परिणाम:", result)

            except Exception as e:

                print("त्रुटि:", str(e))
