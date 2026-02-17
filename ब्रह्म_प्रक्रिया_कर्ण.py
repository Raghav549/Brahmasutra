import threading
import time


class ब्रह्मप्रक्रिया:


    def __init__(self, pid, name, target):

        self.pid = pid

        self.name = name

        self.target = target

        self.thread = threading.Thread(target=self.run)

        self.running = False



    def run(self):

        print("प्रक्रिया प्रारम्भ:", self.name)

        self.running = True

        try:

            self.target()

        except Exception as e:

            print("प्रक्रिया त्रुटि:", e)

        self.running = False

        print("प्रक्रिया समाप्त:", self.name)



    def start(self):

        self.thread.start()



class ब्रह्मप्रक्रियाकर्ण:


    def __init__(self):

        self.processes = {}

        self.next_pid = 1

        print("🕉️ ब्रह्म प्रक्रिया कर्ण सक्रिय")



    def निर्माण(self, name, target):

        pid = self.next_pid

        self.next_pid += 1

        proc = ब्रह्मप्रक्रिया(pid, name, target)

        self.processes[pid] = proc

        print("प्रक्रिया निर्मित:", pid, name)

        return pid



    def प्रारम्भ(self, pid):

        if pid in self.processes:

            self.processes[pid].start()

        else:

            print("त्रुटि: प्रक्रिया नहीं मिली")



    def सूची(self):

        print("प्रक्रिया सूची:")

        for pid, proc in self.processes.items():

            print(pid, proc.name, "running" if proc.running else "stopped")



    def प्रतीक्षा(self):

        while True:

            active = False

            for proc in self.processes.values():

                if proc.running:

                    active = True

            if not active:

                break
            time.sleep(0.1)
