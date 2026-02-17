from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_executable_generator import सूत्रExecutableGenerator
from सूत्र_app_packager import सूत्रAppPackager
from सूत्र_app_loader import सूत्रAppLoader


program = [

    "स्थापित अ 1000",
    "स्थापित ब 500",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]


encoder = सूत्रMachineCode()

machine = encoder.encode(program)


exe_gen = सूत्रExecutableGenerator()

exe_gen.create(machine, "app_exec.सूत्र")


packager = सूत्रAppPackager()

packager.package("app_exec.सूत्र", "calculator")


loader = सूत्रAppLoader()

loader.run("calculator.सूत्रapp")
