from सूत्र_हार्डवेयर_मशीन import सूत्रHardwareMachine

machine = सूत्रHardwareMachine()

program = [

    {"opcode":"LOAD","op1":"अ","op2":100},

    {"opcode":"LOAD","op1":"ब","op2":200},

    {"opcode":"ADD","op1":"अ","op2":"ब"},

    {"opcode":"SHOW","op1":"अ"},

    {"opcode":"STATE"},

    {"opcode":"EXIT"}

]

machine.program_load(program)

machine.execute()

machine.status()
