from ब्रह्म_प्रक्रिया import ब्रह्मप्रक्रियाप्रबंधक


class ब्रह्मअनुसूचक:

    def __init__(self):

        print("🕉️ ब्रह्म अनुसूचक सक्रिय")

        self.pm = ब्रह्मप्रक्रियाप्रबंधक()

        self.queue = []


    def प्रक्रिया_जोड़ो(self,name):

        pid = self.pm.निर्माण(name)

        self.queue.append(pid)

        print("अनुसूचक में जोड़ा:",pid)


    def चलाओ(self):

        print("अनुसूचक प्रारम्भ")

        while len(self.queue) > 0:

            pid = self.queue.pop(0)

            print("CPU दिया गया:",pid)

            self.pm.निष्पादन(pid)

        print("अनुसूचक समाप्त")
