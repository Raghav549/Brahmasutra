# 🕉️ सूत्र Hardware Layer


from सूत्र_device_driver_core import सूत्रDeviceDriver


class सूत्रHardwareLayer:


    def __init__(self):

        print("🕉️ सूत्र Hardware Layer सक्रिय")

        self.driver = सूत्रDeviceDriver()


    def initialize(self):

        self.driver.register("CPU")

        self.driver.register("RAM")

        self.driver.register("DISPLAY")

        self.driver.register("KEYBOARD")


    def show(self):

        self.driver.list()
