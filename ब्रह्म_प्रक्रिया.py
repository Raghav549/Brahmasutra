class ब्रह्मप्रक्रिया:

    def __init__(self, pid, name):

        self.pid = pid

        self.name = name

        self.state = "ready"


class ब्रह्मप्रक्रियाप्रबंधक:

    def __init__(self):

        print("🕉️ ब्रह्म प्रक्रिया प्रबंधक सक्रिय")

        self.processes = {}

        self.next_pid = 1


    def निर्माण(self,name):

        pid = self.next_pid

        process = ब्रह्मप्रक्रिया(pid,name)

        self.processes[pid] = process

        self.next_pid += 1

        print("प्रक्रिया निर्मित:",pid,name)

        return pid


    def सूची(self):

        print("प्रक्रिया सूची:")

        for pid in self.processes:

            p = self.processes[pid]

            print(pid,p.name,p.state)


    def निष्पादन(self,pid):

        if pid not in self.processes:

            print("त्रुटि: प्रक्रिया नहीं मिली")

            return

        process = self.processes[pid]

        process.state = "running"

        print("प्रक्रिया चल रही है:",pid,process.name)

        process.state = "finished"

        print("प्रक्रिया समाप्त:",pid)
