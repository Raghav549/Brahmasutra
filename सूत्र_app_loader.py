# 🕉️ सूत्र Application Loader


from सूत्र_executable_loader import सूत्रExecutableLoader
from सूत्र_machine_cpu import सूत्रMachineCPU


class सूत्रAppLoader:


    def __init__(self):

        print("🕉️ सूत्र App Loader सक्रिय")


    def run(self, app_file):

        with open(app_file, "rb") as f:

            header = f.read(12)

            if header != b"SUTRA_APP_V1":

                print("Invalid app file")
                return


            name_len = int.from_bytes(f.read(1), "big")

            app_name = f.read(name_len).decode("utf-8")

            exe_size = int.from_bytes(f.read(4), "big")

            exe_data = f.read(exe_size)


        temp_exe = "temp_exec.सूत्र"

        with open(temp_exe, "wb") as f:

            f.write(exe_data)


        loader = सूत्रExecutableLoader()

        machine_code = loader.load(temp_exe)


        cpu = सूत्रMachineCPU()

        cpu.run(machine_code)


        print("App executed:", app_name)
