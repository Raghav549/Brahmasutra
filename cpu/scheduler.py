import threading

class कार्य:

    def __init__(self, नाम, क्रिया):
        self.नाम = नाम
        self.क्रिया = क्रिया
        self.स्थिति = "प्रतीक्षा"


class अनुसूचक:

    def __init__(self):
        self.कार्यसूची = []


    def जोड़ें(self, नाम, क्रिया):

        नया_कार्य = कार्य(नाम, क्रिया)
        self.कार्यसूची.append(नया_कार्य)

        print("कार्य जोड़ा गया:", नाम)


    def चलाएँ(self):

        for k in self.कार्यसूची:

            t = threading.Thread(target=self.कार्य_चलाएँ, args=(k,))
            t.start()


    def कार्य_चलाएँ(self, k):

        print("कार्य प्रारम्भ:", k.नाम)

        k.स्थिति = "चल रहा है"

        k.क्रिया()

        k.स्थिति = "समाप्त"

        print("कार्य समाप्त:", k.नाम)
