# 🕉️ सूत्र System Call Manager


from सूत्र_syscall_core import सूत्रSyscallCore


class सूत्रSyscallManager:


    def __init__(self):

        print("🕉️ सूत्र System Call Manager सक्रिय")

        self.core = सूत्रSyscallCore()


    def register(self, name, handler):

        self.core.register(name, handler)


    def invoke(self, name, *args):

        return self.core.call(name, *args)
