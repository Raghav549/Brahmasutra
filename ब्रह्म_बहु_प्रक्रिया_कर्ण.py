print("🕉️ ब्रह्म बहु-प्रक्रिया कर्ण सक्रिय")


from ब्रह्म_प्रक्रिया_निष्पादन_कर्ण import ब्रह्मप्रक्रियानिष्पादनकर्ण


class ब्रह्मबहुप्रक्रियाकर्ण:


    def __init__(self):

        self.kernel = ब्रह्मप्रक्रियानिष्पादनकर्ण()

        self.queue = []


    def प्रक्रिया_निर्माण(self, नाम, आदेश):

        pid = self.kernel.निर्माण(नाम, आदेश)

        self.queue.append(pid)

        print("प्रक्रिया कतार में जोड़ी:", pid)

        return pid


    def अनुसूचन(self):

        print("अनुसूचक प्रारम्भ")

        while self.queue:

            pid = self.queue.pop(0)

            print("CPU प्रक्रिया चला रहा है:", pid)

            self.kernel.निष्पादन(pid)

        print("सभी प्रक्रियाएँ पूर्ण")
