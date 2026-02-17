# 🕉️ Kernel Storage Layer


from सूत्र_kernel_filesystem import सूत्रKernelFileSystem


class सूत्रKernelStorageLayer:


    def __init__(self):

        print("🕉️ Kernel Storage Layer सक्रिय")

        self.fs = सूत्रKernelFileSystem()


    def create(self, name, content):

        self.fs.create(name, content)


    def read(self, name):

        self.fs.read(name)


    def list(self):

        self.fs.list()
