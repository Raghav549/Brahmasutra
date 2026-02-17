import os

def शीर्षक():
    print("===================================")
    print("        सूत्र IDE")
    print("===================================")

def मेनू():
    print("")
    print("1. file चलाओ")
    print("2. compile")
    print("3. APK निर्माण")
    print("4. version")
    print("5. exit")
    print("")

def चलाओ():
    file = input("file नाम: ")
    os.system(f"चलाओ {file}")

def compile():
    file = input("file नाम: ")
    os.system(f"संस्कृत-compile {file}")

def निर्माण():
    file = input("file नाम: ")
    os.system(f"निर्माण {file}")

def version():
    os.system("संस्कृत-version")

while True:
    शीर्षक()
    मेनू()

    choice = input("चयन: ")

    if choice == "1":
        चलाओ()

    elif choice == "2":
        compile()

    elif choice == "3":
        निर्माण()

    elif choice == "4":
        version()

    elif choice == "5":
        break

    else:
        print("अमान्य चयन")
