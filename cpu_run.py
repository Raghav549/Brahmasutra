import सूत्र_cpu_emulator as cpu

processor = cpu.सूत्रCPU()

file = input("Binary file: ")

processor.load_binary(file)

processor.run()
