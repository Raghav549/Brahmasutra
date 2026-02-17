# ब्रह्म संदेश तंत्र

class ब्रह्मसंदेशतंत्र:

    def __init__(self):

        self.श्रोता = {}

        print("🕉️ ब्रह्म संदेश तंत्र सक्रिय")


    def सदस्यता(self, विषय, कार्य):

        if विषय not in self.श्रोता:
            self.श्रोता[विषय] = []

        self.श्रोता[विषय].append(कार्य)

        print(f"सदस्यता जुड़ी: {विषय}")


    def भेजें(self, विषय, संदेश):

        print(f"संदेश भेजा गया: {विषय}")

        if विषय not in self.श्रोता:
            print("कोई श्रोता नहीं")
            return

        for कार्य in self.श्रोता[विषय]:
            कार्य(संदेश)


    def विषय_सूची(self):

        return list(self.श्रोता.keys())
