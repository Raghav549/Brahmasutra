# 🕉️ Kernel Memory Layer


from सूत्र_memory_manager import सूत्रMemoryManager


class सूत्रKernelMemoryLayer:


    def __init__(self):

        print("🕉️ Kernel Memory Layer सक्रिय")

        self.memory = सूत्रMemoryManager()


    def allocate(self, process, size):

        self.memory.allocate(process, size)


    def free(self, process):

        self.memory.free(process)


    def status(self):

        self.memory.status()
