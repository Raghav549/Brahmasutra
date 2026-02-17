# सूत्र तंत्र — Bootloader

print("सूत्र Bootloader आरम्भ")



import time



# boot steps
def boot_sequence():

    print("प्रारम्भिक जाँच...")

    time.sleep(1)


    print("स्मृति जाँच...")

    time.sleep(1)


    print("Kernel लोड हो रहा है...")

    time.sleep(1)


    print("Runtime सक्रिय हो रहा है...")

    time.sleep(1)


    print("सूत्र प्रणाली तैयार")



# start kernel
def kernel_start():

    print("Kernel प्रारम्भ")


# start system
def system_start():

    boot_sequence()

    kernel_start()

    print("सूत्र OS सक्रिय")



# main
if __name__ == "__main__":

    system_start()
