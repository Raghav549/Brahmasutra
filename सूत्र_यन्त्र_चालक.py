# 🕉️ सूत्र यन्त्र चालक तंत्र


class यन्त्रचालक:


    def __init__(self):

        self.उपकरण = {}

        print("🕉️ यन्त्र चालक तंत्र सक्रिय")


    def पंजीकरण(self, नाम, कार्य):

        self.उपकरण[नाम] = कार्य

        print("उपकरण पंजीकृत:", नाम)


    def उपयोग(self, नाम, डेटा=None):

        if नाम not in self.उपकरण:

            print("त्रुटि: उपकरण नहीं मिला")

            return None


        return self.उपकरण[नाम](डेटा)
