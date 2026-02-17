# 🕉️ सूत्र Process Core


class सूत्रProcess:


    def __init__(self, pid, code):

        self.pid = pid
        self.code = code
        self.memory = {}

        print(f"Process created: PID {pid}")


    def run(self):

        print(f"Running process: {self.pid}")

        exec(self.code, {}, self.memory)
