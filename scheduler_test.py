from सूत्र_process_manager_v2 import सूत्रProcessManager
from सूत्र_scheduler import सूत्रScheduler


manager = सूत्रProcessManager()
scheduler = सूत्रScheduler()


code1 = '''
print("App 1 running")
'''

code2 = '''
print("App 2 running")
'''

code3 = '''
print("AI engine running")
'''


pid1 = manager.create(code1)
pid2 = manager.create(code2)
pid3 = manager.create(code3)


scheduler.add_process(manager.processes[pid1])
scheduler.add_process(manager.processes[pid2])
scheduler.add_process(manager.processes[pid3])


scheduler.run()
