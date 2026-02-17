# 🕉️ सूत्र Kernel Application Layer


from सूत्र_app_manager import सूत्रAppManager


class सूत्रKernelAppLayer:


    def __init__(self):

        print("🕉️ सूत्र Kernel App Layer सक्रिय")

        self.manager = सूत्रAppManager()


    def install_app(self, app):

        print("Kernel installing app")

        self.manager.install(app)


    def run_app(self, app):

        print("Kernel running app")

        self.manager.run(app)


    def list_apps(self):

        print("Kernel listing apps")

        self.manager.list_apps()


    def remove_app(self, app):

        print("Kernel removing app")

        self.manager.uninstall(app)
