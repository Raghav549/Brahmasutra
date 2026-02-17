# 🕉️ सूत्र Kernel Binary Loader

import सूत्र_binary_loader as binary_loader


class KernelBinaryLoader:


    def __init__(self):

        print("🕉️ सूत्र Kernel Binary Loader सक्रिय")

        self.loader = binary_loader.BinaryLoader()


    def चलाओ(self, संचिका):

        print("Kernel binary execution प्रारम्भ")

        self.loader.लोड(संचिका)
