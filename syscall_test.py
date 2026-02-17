from सूत्र_syscall_manager import सूत्रSyscallManager


manager = सूत्रSyscallManager()


def show_message(msg):

    print("Kernel says:", msg)


manager.register("SHOW", show_message)


manager.invoke("SHOW", "Hello from user mode")
