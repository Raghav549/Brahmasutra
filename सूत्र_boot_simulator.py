# 🕉️ सूत्र Boot Simulator


import struct
import सूत्र_os_loader as loader


IMAGE = "सूत्र.img"


class BootSimulator:


    def __init__(self):

        print("🕉️ सूत्र Boot Simulator प्रारम्भ")


    def boot(self):

        print("Boot image लोड हो रहा है...")

        try:

            with open(IMAGE, "rb") as f:

                signature = f.read(7)

                if signature != b"SUTRAOS":

                    print("अमान्य image")
                    return


                version = struct.unpack("I", f.read(4))[0]

                print("Version:", version)


                kernel_size = struct.unpack("I", f.read(4))[0]

                kernel_data = f.read(kernel_size)


                print("Kernel लोड सफल")


                with open("boot_kernel.bin", "wb") as k:

                    k.write(kernel_data)


                print("Kernel execute हो रहा है...")


                os = loader.OSLoader()

                os.चलाओ("boot_kernel.bin")


        except FileNotFoundError:

            print("image नहीं मिला")


sim = BootSimulator()

sim.boot()
