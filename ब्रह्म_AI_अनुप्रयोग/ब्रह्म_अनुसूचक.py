# ब्रह्म अनुसूचक (Scheduler)

import time
import threading


class ब्रह्मअनुसूचक:

    def __init__(self):

        self.कार्यसूची = []

        self.चल_रहा = False

        print("⏳ ब्रह्म अनुसूचक सक्रिय")


    def जोड़ो(self, नाम, कार्य):

        self.कार्यसूची.append({
            "name": नाम,
            "task": कार्य,
            "status": "waiting"
        })

        return {
            "status": "added",
            "task": नाम
        }


    def चलाओ(self):

        self.चल_रहा = True

        while self.चल_रहा:

            if len(self.कार्यसूची) == 0:

                time.sleep(1)

                continue

            task = self.कार्यसूची.pop(0)

            task["status"] = "running"

            print("चल रहा:", task["name"])

            try:

                task["task"]()

                print("पूर्ण:", task["name"])

            except Exception as e:

                print("त्रुटि:", e)

            time.sleep(0.1)


    def प्रारम्भ(self):

        thread = threading.Thread(target=self.चलाओ)

        thread.daemon = True

        thread.start()

        return {
            "status": "started"
        }


    def रोकें(self):

        self.चल_रहा = False

        return {
            "status": "stopped"
        }


    def सूची(self):

        return self.कार्यसूची
