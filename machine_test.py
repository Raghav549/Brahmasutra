from सूत्र_machine_code import सूत्रMachineCode

program = [

    "स्थापित अ 50",
    "स्थापित ब 10",
    "योग अ ब",
    "दर्शय अ",
    "निर्गम"

]

encoder = सूत्रMachineCode()

machine = encoder.encode(program)

print(machine)
