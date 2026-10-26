# 🕉️ सूत्र अनुसूचक (round-robin scheduler)
#
# The original loop was ``while True`` and never terminated, which made the
# demo hang. It now runs a bounded number of rounds (default 3) and stops
# early when nothing is active.

import time


class कार्य:
    def __init__(self, नाम, कार्यफल):
        self.नाम = नाम
        self.कार्यफल = कार्यफल
        self.सक्रिय = True
        self.चक्र = 0


class सूत्रअनुसूचक:
    def __init__(self, चरम_चक्र=3, विराम=0.0):
        self.कार्यसूची = []
        self.चरम_चक्र = चरम_चक्र
        self.विराम = विराम
        print("🕉️ सूत्र अनुसूचक सक्रिय")

    # -- registration ----------------------------------------------------
    def जोड़(self, नाम, कार्यफल):
        if not callable(कार्यफल):
            raise TypeError(f"कार्य '{नाम}' के लिए कॉलबल चाहिए")
        नया = कार्य(नाम, कार्यफल)
        self.कार्यसूची.append(नया)
        print("कार्य जोड़ा:", नाम)
        return नया

    def हटाओ(self, नाम):
        for क in list(self.कार्यसूची):
            if क.नाम == नाम:
                क.सक्रिय = False
                self.कार्यसूची.remove(क)
                print("कार्य हटाया:", नाम)
                return True
        return False

    # -- execution -------------------------------------------------------
    def चलाओ(self, चक्र=None):
        चक्र = self.चरम_चक्र if चक्र is None else चक्र
        print("अनुसूचक प्रारम्भ")
        for _ in range(चक्र):
            सक्रिय = [क for क in self.कार्यसूची if क.सक्रिय]
            if not सक्रिय:
                print("कोई सक्रिय कार्य नहीं")
                break
            for क in सक्रिय:
                print("चल रहा:", क.नाम)
                क.कार्यफल()
                क.चक्र += 1
                if self.विराम:
                    time.sleep(self.विराम)
        print("अनुसूचक समाप्त")
        return len(self.कार्यसूची)
