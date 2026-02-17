import time

from ब्रह्म_प्रक्रिया_प्रबंधक import ब्रह्मप्रक्रियाप्रबंधक



class ब्रह्मCPUअनुसूचक:

    def __init__(self):

        self.प्रबंधक = ब्रह्मप्रक्रियाप्रबंधक()

        self.queue = []

        print("🕉️ ब्रह्म CPU अनुसूचक सक्रिय")



    def जोड़ो(self, नाम, कार्य):

        pid = self.प्रबंधक.निर्माण(नाम, कार्य)

        self.queue.append(pid)

        print("कार्य जोड़ा:", नाम)



    def चलाओ(self):

        print("CPU scheduling प्रारम्भ")

        while self.queue:

            pid = self.queue.pop(0)

            print("चल रहा है:", pid)

            self.प्रबंधक.चलाओ(pid)

            time.sleep(0.5)

        print("CPU scheduling समाप्त")
