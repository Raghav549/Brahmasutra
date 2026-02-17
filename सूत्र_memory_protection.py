# 🕉️ सूत्र Memory Protection System


class सूत्रMemoryProtection:


    def __init__(self):

        print("🕉️ सूत्र Memory Protection सक्रिय")

        self.memory_space = {}


    def allocate(self, pid):

        print(f"Memory allocated for PID {pid}")

        self.memory_space[pid] = {}


    def write(self, pid, key, value):

        if pid not in self.memory_space:

            print("Memory access denied")

            return

        self.memory_space[pid][key] = value


    def read(self, pid, key):

        if pid not in self.memory_space:

            print("Memory access denied")

            return None

        return self.memory_space[pid].get(key)


    def show(self):

        print("Protected memory map:")
        print(self.memory_space)
