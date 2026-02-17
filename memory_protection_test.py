from सूत्र_process_manager_v2 import सूत्रProcessManager
from सूत्र_memory_protection import सूत्रMemoryProtection


manager = सूत्रProcessManager()
memory = सूत्रMemoryProtection()


pid1 = manager.create("print('Process 1')")
pid2 = manager.create("print('Process 2')")


memory.allocate(pid1)
memory.allocate(pid2)


memory.write(pid1, "data", "secret_app1")
memory.write(pid2, "data", "secret_app2")


print("PID1 memory:", memory.read(pid1, "data"))
print("PID2 memory:", memory.read(pid2, "data"))


memory.show()
