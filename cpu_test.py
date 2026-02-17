from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU


program = [

    "स्थापित अ 50",
    "स्थापित ब 20",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]


encoder = सूत्रMachineCode()

machine = encoder.encode(program)


cpu = सूत्रMachineCPU()

cpu.run(machine)
