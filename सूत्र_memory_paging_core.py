# 🕉️ सूत्र Memory Paging Core


class सूत्रMemoryPaging:


    def __init__(self):

        print("🕉️ सूत्र Memory Paging सक्रिय")

        self.page_size = 256

        self.pages = {}


    def allocate(self, process, data):

        pages_needed = len(data) // self.page_size + 1

        self.pages[process] = {

            "pages": pages_needed,

            "data": data

        }

        print(f"Memory allocated: {process} → {pages_needed} pages")


    def read(self, process):

        if process in self.pages:

            return self.pages[process]["data"]

        else:

            print("Memory not found")


    def status(self):

        print("Memory Pages:")

        for p in self.pages:

            print(p, "→", self.pages[p]["pages"], "pages")
