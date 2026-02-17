from सूत्र_memory_manager_v2 import सूत्रMemoryManagerV2


mem = सूत्रMemoryManagerV2()


mem.allocate("process1", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


mem.allocate("process2", "1234567890")


mem.status()
