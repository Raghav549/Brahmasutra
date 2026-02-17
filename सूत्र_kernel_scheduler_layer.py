# 🕉️ Kernel Scheduler Layer


from सूत्र_scheduler import सूत्रScheduler


class सूत्रKernelSchedulerLayer:


    def __init__(self):

        print("🕉️ Kernel Scheduler Layer सक्रिय")

        self.scheduler = सूत्रScheduler()


    def add_process(self, process):

        self.scheduler.add(process)


    def run(self):

        self.scheduler.run()
