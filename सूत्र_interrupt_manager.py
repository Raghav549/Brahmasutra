# 🕉️ सूत्र Interrupt Manager


from सूत्र_interrupt_core import सूत्रInterruptCore


class सूत्रInterruptManager:


    def __init__(self):

        print("🕉️ सूत्र Interrupt Manager सक्रिय")

        self.core = सूत्रInterruptCore()


    def register(self, interrupt, handler):

        self.core.register(interrupt, handler)


    def trigger(self, interrupt):

        self.core.trigger(interrupt)
