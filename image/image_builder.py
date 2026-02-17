import os

class सूत्रImageBuilder:

    def __init__(self):

        self.image_path = os.path.expanduser("~/सूत्र-तंत्र/सूत्रOS.img")

    def निर्माण(self):

        print("सूत्र OS Image निर्माण प्रारम्भ")

        with open(self.image_path, "w", encoding="utf-8") as img:

            img.write("SUTRA_OS_IMAGE\n")

            img.write("BOOTLOADER\n")

            img.write("KERNEL\n")

            img.write("MEMORY\n")

            img.write("CPU\n")

            img.write("VM\n")

            img.write("RUNTIME\n")

            img.write("DESKTOP\n")

            img.write("STORE\n")

        print("Image निर्माण सफल")

        print("Image स्थान:", self.image_path)
