from सूत्र_वास्तविक_CPU import सूत्रCPU

cpu = सूत्रCPU()

program = [

    {"opcode":"LOAD","op1":"अ","op2":10},

    {"opcode":"LOAD","op1":"ब","op2":20},

    {"opcode":"ADD","op1":"अ","op2":"ब"},

    {"opcode":"SHOW","op1":"अ"},

    {"opcode":"STATE"},

    {"opcode":"EXIT"}

]

cpu.EXECUTE(program)
