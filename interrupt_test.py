from सूत्र_interrupt_manager import सूत्रInterruptManager


manager = सूत्रInterruptManager()


def keyboard_interrupt():

    print("Keyboard interrupt handled")


def system_call_interrupt():

    print("System call interrupt handled")


manager.register("KEYBOARD", keyboard_interrupt)

manager.register("SYSCALL", system_call_interrupt)


manager.trigger("KEYBOARD")

manager.trigger("SYSCALL")
