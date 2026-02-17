from सूत्र_process_manager_v2 import सूत्रProcessManager


manager = सूत्रProcessManager()


code1 = '''
x = 10
print("Process 1:", x)
'''

code2 = '''
x = 50
print("Process 2:", x)
'''


pid1 = manager.create(code1)
pid2 = manager.create(code2)


manager.run(pid1)
manager.run(pid2)
