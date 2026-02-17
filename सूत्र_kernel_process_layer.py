# 🕉️ सूत्र Kernel Process Layer


from सूत्र_process_manager import सूत्रProcessManager


class सूत्रKernelProcessLayer:


    def __init__(self):

        print("🕉️ Kernel Process Layer सक्रिय")

        self.manager = सूत्रProcessManager()


    def run_app(self, app):

        pid = self.manager.create(app)

        return pid


    def list_processes(self):

        self.manager.list()


    def stop_process(self, pid):

        self.manager.stop(pid)


    def remove_process(self, pid):

        self.manager.remove(pid)
