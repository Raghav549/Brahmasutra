# 🕉️ सूत्र Scheduler System


import time


class सूत्रScheduler:


    def __init__(self):

        print("🕉️ सूत्र Scheduler सक्रिय")

        self.queue = []


    def add_process(self, process):

        print(f"Process added to scheduler: {process.pid}")

        self.queue.append(process)


    def run(self):

        print("🕉️ Scheduler starting execution")

        while self.queue:

            process = self.queue.pop(0)

            print(f"Scheduling process: {process.pid}")

            process.run()

            time.sleep(0.5)

        print("🕉️ Scheduler execution complete")
