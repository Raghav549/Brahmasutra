# 🕉️ सूत्र Interrupt Core


class सूत्रInterruptCore:


    def __init__(self):

        print("🕉️ सूत्र Interrupt Core सक्रिय")

        self.handlers = {}


    def register(self, interrupt, handler):

        self.handlers[interrupt] = handler

        print(f"Interrupt registered: {interrupt}")


    def trigger(self, interrupt):

        print(f"Interrupt triggered: {interrupt}")

        if interrupt in self.handlers:

            self.handlers[interrupt]()

        else:

            print("No handler found")
