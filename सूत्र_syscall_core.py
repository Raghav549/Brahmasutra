# 🕉️ सूत्र System Call Core


class सूत्रSyscallCore:


    def __init__(self):

        print("🕉️ सूत्र System Call Core सक्रिय")

        self.syscalls = {}


    def register(self, name, handler):

        self.syscalls[name] = handler

        print(f"Syscall registered: {name}")


    def call(self, name, *args):

        print(f"Syscall invoked: {name}")

        if name in self.syscalls:

            return self.syscalls[name](*args)

        else:

            print("Syscall not found")
