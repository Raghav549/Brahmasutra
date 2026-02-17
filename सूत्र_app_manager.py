# 🕉️ सूत्र Application Manager


import os
import shutil


from सूत्र_app_loader import सूत्रAppLoader


class सूत्रAppManager:


    def __init__(self):

        self.install_dir = os.path.expanduser("~/सूत्र-तंत्र/installed_apps")

        os.makedirs(self.install_dir, exist_ok=True)

        print("🕉️ सूत्र App Manager सक्रिय")


    def install(self, app_file):

        name = os.path.basename(app_file)

        dest = os.path.join(self.install_dir, name)

        shutil.copy(app_file, dest)

        print("Installed:", name)


    def uninstall(self, app_name):

        path = os.path.join(self.install_dir, app_name)

        if os.path.exists(path):

            os.remove(path)

            print("Removed:", app_name)

        else:

            print("App not found")


    def list_apps(self):

        apps = os.listdir(self.install_dir)

        print("Installed Apps:")

        for app in apps:

            print("•", app)


    def run(self, app_name):

        path = os.path.join(self.install_dir, app_name)

        if not os.path.exists(path):

            print("App not installed")

            return


        loader = सूत्रAppLoader()

        loader.run(path)
