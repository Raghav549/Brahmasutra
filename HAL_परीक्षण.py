from सूत्र_HAL import सूत्रHAL
from सूत्र_CPU_HAL import CPU
from सूत्र_स्मृति_HAL import स्मृति


hal = सूत्रHAL()


cpu = CPU()
memory = स्मृति()


hal.पंजीकरण("CPU", cpu)
hal.पंजीकरण("स्मृति", memory)


cpu.स्थापित("अ", 100)

print("CPU मान:", cpu.प्राप्त("अ"))


memory.लिख(0, 999)

print("Memory मान:", memory.पढ़(0))
