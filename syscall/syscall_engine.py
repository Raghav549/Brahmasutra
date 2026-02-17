class सूत्र_SystemCall:


    def __init__(self):

        self.calls = {

            "process_create": self.process_create,

            "memory_allocate": self.memory_allocate,

            "cpu_execute": self.cpu_execute,

            "process_list": self.process_list

        }


    def invoke(self, name, *args):

        if name in self.calls:

            return self.calls[name](*args)

        else:

            print("अज्ञात system call:", name)


    def process_create(self, name):

        print("System Call: प्रक्रिया निर्माण:", name)


    def memory_allocate(self, size):

        print("System Call: स्मृति आवंटन:", size)


    def cpu_execute(self, task):

        print("System Call: CPU execution:", task)


    def process_list(self):

        print("System Call: प्रक्रिया सूची")
