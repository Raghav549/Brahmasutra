# 🕉️ सूत्र Process Manager v2


from सूत्र_process_core import सूत्रProcess


class सूत्रProcessManager:


    def __init__(self):

        print("🕉️ सूत्र Process Manager v2 सक्रिय")

        self.processes = {}
        self.next_pid = 1


    def create(self, code):

        pid = self.next_pid

        process = सूत्रProcess(pid, code)

        self.processes[pid] = process

        self.next_pid += 1

        return pid


    def run(self, pid):

        if pid in self.processes:

            self.processes[pid].run()

        else:

            print("Process not found")
