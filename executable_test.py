from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU
from सूत्र_executable_generator import सूत्रExecutableGenerator
from सूत्र_executable_loader import सूत्रExecutableLoader


program = [

    "स्थापित अ 500",
    "स्थापित ब 250",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]


encoder = सूत्रMachineCode()

machine = encoder.encode(program)


generator = सूत्रExecutableGenerator()

generator.create(machine, "hello.सूत्र")


loader = सूत्रExecutableLoader()

loaded = loader.load("hello.सूत्र")


cpu = सूत्रMachineCPU()

cpu.run(loaded)
