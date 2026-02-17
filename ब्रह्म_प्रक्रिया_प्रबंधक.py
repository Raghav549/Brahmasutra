import uuid

class ब्रह्मप्रक्रिया:

    def __init__(self, नाम, कार्य):

        self.id = str(uuid.uuid4())

        self.नाम = नाम

        self.कार्य = कार्य

        self.स्थिति = "तैयार"



class ब्रह्मप्रक्रियाप्रबंधक:

    def __init__(self):

        self.प्रक्रियाएँ = {}

        print("🕉️ ब्रह्म प्रक्रिया प्रबंधक सक्रिय")



    def निर्माण(self, नाम, कार्य):

        p = ब्रह्मप्रक्रिया(नाम, कार्य)

        self.प्रक्रियाएँ[p.id] = p

        print(f"प्रक्रिया निर्मित: {नाम} | ID: {p.id}")

        return p.id



    def चलाओ(self, id):

        if id in self.प्रक्रियाएँ:

            p = self.प्रक्रियाएँ[id]

            p.स्थिति = "चल रही"

            print(f"प्रक्रिया चल रही: {p.नाम}")

            exec(p.कार्य)

            p.स्थिति = "समाप्त"

        else:

            print("त्रुटि: प्रक्रिया नहीं मिली")



    def सूची(self):

        print("प्रक्रिया सूची:")

        for id, p in self.प्रक्रियाएँ.items():

            print(f"{p.नाम} | {p.स्थिति} | {id}")
