# 🕉️ सूत्र Application Packager


class सूत्रAppPackager:


    def __init__(self):

        print("🕉️ सूत्र App Packager सक्रिय")


    def package(self, executable_file, app_name):

        package_file = app_name + ".सूत्रapp"

        with open(executable_file, "rb") as exe:

            exe_data = exe.read()


        with open(package_file, "wb") as pkg:

            pkg.write(b"SUTRA_APP_V1")

            name_bytes = app_name.encode("utf-8")

            pkg.write(len(name_bytes).to_bytes(1, "big"))

            pkg.write(name_bytes)

            pkg.write(len(exe_data).to_bytes(4, "big"))

            pkg.write(exe_data)


        print("App packaged:", package_file)
