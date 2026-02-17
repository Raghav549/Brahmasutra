# 🕉️ सूत्र Memory Manager


class सूत्रMemoryManager:


    def __init__(self):

        print("🕉️ सूत्र Memory Manager सक्रिय")

        self.memory = {}

        self.total = 1024   # 1024 blocks simulated RAM


    def allocate(self, process, size):

        if len(self.memory) + size > self.total:

            print("Memory full")

            return False


        for i in range(size):

            addr = f"{process}_{i}"

            self.memory[addr] = process


        print(f"Memory allocated: {process} → {size}")

        return True


    def free(self, process):

        remove = []

        for addr in self.memory:

            if self.memory[addr] == process:

                remove.append(addr)


        for addr in remove:

            del self.memory[addr]


        print(f"Memory freed: {process}")


    def status(self):

        used = len(self.memory)

        free = self.total - used

        print(f"RAM Used: {used}")

        print(f"RAM Free: {free}")
