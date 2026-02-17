# सूत्र तंत्र — REPL (Real-time Sanskrit Console)

from निर्वाहक import निर्वाह


def सूत्र_REPL():

    print("🕉️ सूत्र REPL सक्रिय")
    print("निर्गच्छ लिखकर बाहर जाएं")

    while True:

        आदेश = input("सूत्र> ")

        आदेश = आदेश.strip()

        if आदेश == "निर्गच्छ":

            print("सूत्र समाप्त")
            break

        if आदेश == "":
            continue

        try:

            निर्वाह(आदेश)

        except Exception as त्रुटि:

            print("त्रुटि:", त्रुटि)


def परीक्षण():

    सूत्र_REPL()


if __name__ == "__main__":
    परीक्षण()
