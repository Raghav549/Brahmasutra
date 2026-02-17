from सूत्र_machine_code import सूत्रMachineCode
from सूत्र_machine_cpu import सूत्रMachineCPU
from सूत्र_binary_generator import सूत्रBinaryGenerator
from सूत्र_binary_loader import सूत्रBinaryLoader


program = [

    "स्थापित अ 100",
    "स्थापित ब 25",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]


encoder = सूत्रMachineCode()

machine = encoder.encode(program)


generator = सूत्रBinaryGenerator()

generator.save(machine, "test.bin")


loader = सूत्रBinaryLoader()

loaded_machine = loader.load("test.bin")


cpu = सूत्रMachineCPU()

cpu.run(loaded_machine)
