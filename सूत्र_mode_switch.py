# 🕉️ सूत्र Mode Switch System


from सूत्र_kernel_mode import सूत्रKernelMode
from सूत्र_user_mode import सूत्रUserMode


class सूत्रModeSwitch:


    def __init__(self):

        print("🕉️ Mode Switch System सक्रिय")

        self.kernel = सूत्रKernelMode()

        self.user = सूत्रUserMode()


    def run_kernel_task(self, task):

        print("Switching to Kernel Mode")

        self.kernel.execute_kernel(task)


    def run_user_app(self, app):

        print("Switching to User Mode")

        self.user.execute_user_app(app)
