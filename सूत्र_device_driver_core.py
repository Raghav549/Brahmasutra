# 🕉️ सूत्र Device Driver Core


class सूत्रDeviceDriver:


    def __init__(self):

        print("🕉️ सूत्र Device Driver Core सक्रिय")

        self.devices = {}


    def register(self, name):

        self.devices[name] = "active"

        print(f"Device registered: {name}")


    def status(self, name):

        if name in self.devices:

            print(f"{name}: active")

        else:

            print(f"{name}: not found")


    def list(self):

        print("Devices:")

        for d in self.devices:

            print(d)
