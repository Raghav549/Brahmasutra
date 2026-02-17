# 🕉️ ब्रह्म डेमन प्रबंधक

import threading
import time

class ब्रह्मडेमनप्रबंधक:

    def __init__(self):

        print("🕉️ ब्रह्म डेमन प्रबंधक सक्रिय")

        self.डेमन = {}

    def जोड़ें(self, नाम, कार्य, अंतराल=1):

        if नाम in self.डेमन:

            print("डेमन पहले से मौजूद:", नाम)

            return

        daemon = {

            "नाम": नाम,
            "कार्य": कार्य,
            "अंतराल": अंतराल,
            "चल_रहा": True,
            "thread": None

        }

        thread = threading.Thread(
            target=self._चलाएँ,
            args=(daemon,),
            daemon=True
        )

        daemon["thread"] = thread

        self.डेमन[नाम] = daemon

        thread.start()

        print("डेमन शुरू:", नाम)

    def _चलाएँ(self, daemon):

        while daemon["चल_रहा"]:

            try:

                daemon["कार्य"]()

            except Exception as e:

                print("डेमन त्रुटि:", daemon["नाम"], e)

            time.sleep(daemon["अंतराल"])

    def रोकें(self, नाम):

        if नाम not in self.डेमन:

            print("डेमन नहीं मिला:", नाम)

            return

        self.डेमन[नाम]["चल_रहा"] = False

        print("डेमन रोका:", नाम)

    def सूची(self):

        print("\nसक्रिय डेमन:\n")

        for नाम in self.डेमन:

            स्थिति = "चल रहा" if self.डेमन[नाम]["चल_रहा"] else "रुका"

            print(f"{नाम} : {स्थिति}")
