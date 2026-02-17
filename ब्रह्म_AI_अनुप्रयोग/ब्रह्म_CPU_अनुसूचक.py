# ब्रह्म CPU अनुसूचक तंत्र
# VERSION 59

import threading
import time
import queue
import uuid


class ब्रह्मCPUअनुसूचक:

    def __init__(self):

        self.प्रक्रिया_पंक्ति = queue.Queue()

        self.चल_रहा = False

        self.सक्रिय_प्रक्रिया = None

        self.lock = threading.Lock()

        print("⚙️ ब्रह्म CPU अनुसूचक सक्रिय")


    # नई प्रक्रिया जोड़ें
    def जोड़ें(self, कार्य, नाम="प्रक्रिया"):

        process_id = str(uuid.uuid4())

        process = {
            "id": process_id,
            "name": नाम,
            "task": कार्य,
            "status": "ready"
        }

        self.प्रक्रिया_पंक्ति.put(process)

        print(f"📥 प्रक्रिया जोड़ी गई: {नाम}")

        return process_id


    # scheduler loop
    def चालू(self):

        if self.चल_रहा:
            return

        self.चल_रहा = True

        thread = threading.Thread(target=self.loop)

        thread.daemon = True

        thread.start()

        print("🚀 CPU Scheduler चालू")


    # scheduler loop core
    def loop(self):

        while self.चल_रहा:

            if not self.प्रक्रिया_पंक्ति.empty():

                process = self.प्रक्रिया_पंक्ति.get()

                self.सक्रिय_प्रक्रिया = process

                print(f"▶️ प्रक्रिया चालू: {process['name']}")

                try:

                    process["status"] = "running"

                    process["task"]()

                    process["status"] = "completed"

                    print(f"✅ प्रक्रिया पूर्ण: {process['name']}")

                except Exception as e:

                    process["status"] = "error"

                    print(f"❌ त्रुटि: {e}")

                self.सक्रिय_प्रक्रिया = None

            else:

                time.sleep(0.1)


    # scheduler stop
    def रोकें(self):

        self.चल_रहा = False

        print("🛑 CPU Scheduler बंद")


    # status
    def स्थिति(self):

        return {
            "running": self.चल_रहा,
            "current": self.सक्रिय_प्रक्रिया
        }
