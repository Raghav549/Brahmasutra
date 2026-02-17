import threading
import time

class प्रक्रिया:

    def __init__(self, नाम, क्रिया):

        self.नाम = नाम
        self.क्रिया = क्रिया

        self.pid = id(self)

        self.स्थिति = "नया"


    def चलाएँ(self):

        print("प्रक्रिया प्रारम्भ:", self.नाम, "PID:", self.pid)

        self.स्थिति = "चल रहा है"

        self.क्रिया()

        self.स्थिति = "समाप्त"

        print("प्रक्रिया समाप्त:", self.नाम)



class प्रक्रिया_प्रबंधक:

    def __init__(self):

        self.प्रक्रियाएँ = {}


    def बनाएँ(self, नाम, क्रिया):

        p = प्रक्रिया(नाम, क्रिया)

        self.प्रक्रियाएँ[p.pid] = p

        print("प्रक्रिया बनी:", नाम, "PID:", p.pid)

        return p.pid


    def चलाएँ(self, pid):

        if pid in self.प्रक्रियाएँ:

            p = self.प्रक्रियाएँ[pid]

            t = threading.Thread(target=p.चलाएँ)

            t.start()

        else:

            print("PID नहीं मिला")


    def सूची(self):

        print("प्रक्रिया सूची:")

        for pid, p in self.प्रक्रियाएँ.items():

            print(pid, p.नाम, p.स्थिति)
