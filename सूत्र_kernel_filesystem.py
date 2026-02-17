# 🕉️ सूत्र Kernel File System


import os


class सूत्रKernelFileSystem:


    def __init__(self):

        print("🕉️ सूत्र Kernel File System सक्रिय")

        self.root = os.path.expanduser("~/सूत्र-तंत्र/भंडार")

        os.makedirs(self.root, exist_ok=True)


    def create(self, name, content):

        path = os.path.join(self.root, name)

        with open(path, "w", encoding="utf-8") as f:

            f.write(content)

        print(f"File created: {path}")


    def read(self, name):

        path = os.path.join(self.root, name)

        if not os.path.exists(path):

            print("File not found")

            return

        with open(path, "r", encoding="utf-8") as f:

            data = f.read()

        print(f"File content:\n{data}")


    def list(self):

        print("Stored files:")

        for file in os.listdir(self.root):

            print("•", file)
