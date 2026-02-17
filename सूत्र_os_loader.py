# 🕉️ सूत्र OS Loader


from सूत्र_binary_loader import सूत्रBinaryLoader


class सूत्रOSLoader:


    def __init__(self):

        print("🕉️ सूत्र Operating System Loader सक्रिय")

        self.loader = सूत्रBinaryLoader()


    def run_program(self, file):

        print("OS program execution प्रारम्भ")

        self.loader.load_and_run(file)

        print("OS execution समाप्त")
