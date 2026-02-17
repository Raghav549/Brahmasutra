# सूत्र तंत्र — सूत्र शेल
# Sanskrit Command Shell

print("सूत्र शेल आरम्भ")



# system state
सक्रिय = True



# commands

def सहायता():

    print("उपलब्ध आदेश:")

    print("सहायता")
    print("स्थिति")
    print("समय")
    print("निर्गम")



def स्थिति():

    print("सूत्र तंत्र सक्रिय है")



def समय():

    import time

    print("समय:", time.ctime())



def निर्गम():

    global सक्रिय

    सक्रिय = False

    print("सूत्र शेल समाप्त")



# command registry
आदेश = {

    "सहायता": सहायता,
    "स्थिति": स्थिति,
    "समय": समय,
    "निर्गम": निर्गम

}



# shell loop
def शेल():

    print("सूत्र तंत्र में स्वागत")

    while सक्रिय:

        इनपुट = input("सूत्र > ")

        if इनपुट in आदेश:

            आदेश[इनपुट]()

        else:

            print("अज्ञात आदेश")



# start shell
शेल()
