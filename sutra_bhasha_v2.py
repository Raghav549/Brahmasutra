import os
import webbrowser

print("🕉️ सूत्रभाषा v2 सक्रिय")

HOME = os.path.expanduser("~")

while True:

    आदेश = input("सूत्र >>> ").strip()

    # प्रदर्शय = print
    if आदेश.startswith("प्रदर्शय"):
        text = आदेश.replace("प्रदर्शय", "").strip()
        print(text)


    # निर्मापय = create file
    elif आदेश.startswith("निर्मापय"):

        parts = आदेश.split()

        if len(parts) >= 2:

            filename = parts[1]
            path = os.path.join(HOME, filename)

            with open(path, "w") as f:
                f.write("सूत्रभाषा द्वारा निर्मित")

            print(f"{filename} निर्मित")


    # उद्घाटय = open file
    elif आदेश.startswith("उद्घाटय"):

        parts = आदेश.split()

        if len(parts) >= 2:

            filename = parts[1]
            path = os.path.join(HOME, filename)

            os.system(f"termux-open '{path}'")

            print(f"{filename} उद्घाटित")


    # सूची = list files
    elif आदेश == "सूची":

        files = os.listdir(HOME)

        for f in files:
            print(f)


    # समय = show time
    elif आदेश == "समय":

        os.system("date")


    # स्वच्छ = clear screen
    elif आदेश == "स्वच्छ":

        os.system("clear")


    # निर्गच्छ = exit
    elif आदेश == "निर्गच्छ":

        print("सूत्रभाषा समाप्त")
        break


    else:

        print("अज्ञात आदेश")
