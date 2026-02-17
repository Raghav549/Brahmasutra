import threading

from ब्रह्म_प्रक्रिया_प्रबंधक import ब्रह्मप्रक्रियाप्रबंधक



class ब्रह्मबहुकार्यतंत्र:

    def __init__(self):

        self.प्रबंधक = ब्रह्मप्रक्रियाप्रबंधक()

        self.threads = []

        print("🕉️ ब्रह्म बहुकार्य तंत्र सक्रिय")



    def नया_कार्य(self, नाम, कार्य):

        pid = self.प्रबंधक.निर्माण(नाम, कार्य)

        t = threading.Thread(target=self.प्रबंधक.चलाओ, args=(pid,))

        self.threads.append(t)

        t.start()



    def प्रतीक्षा(self):

        for t in self.threads:

            t.join()

        print("सभी कार्य पूर्ण")
