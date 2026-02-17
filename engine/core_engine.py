import os

चर = {}
क्रियाएँ = {}

def सूत्र_पढ़ें(file):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    return [line.strip() for line in lines if line.strip()]


def क्रिया_पंजीकरण(lines):

    current = None
    body = []

    for line in lines:

        if line.startswith("क्रिया"):

            current = line.replace("क्रिया","").replace(":","").strip()
            body = []

        elif line == "समाप्त":

            if current:
                क्रियाएँ[current] = body
            current = None

        elif current:

            body.append(line)


def क्रिया_निष्पादन(name):

    if name in क्रियाएँ:

        return क्रियाएँ[name]

    return []


def सूत्र_व्याख्या(lines):

    क्रिया_पंजीकरण(lines)

    output = []

    i = 0

    while i < len(lines):

        line = lines[i]

        if line.startswith("पाठ"):

            text = line.replace("पाठ","").strip().strip('"')
            print(text)
            output.append(text)

        elif line.startswith("यदि"):

            condition = line.replace("यदि","").replace(":","").strip()

            if condition == "सत्य":

                i += 1
                while i < len(lines) and lines[i] != "समाप्त":

                    inner = lines[i]

                    if inner.startswith("पाठ"):
                        text = inner.replace("पाठ","").strip().strip('"')
                        print(text)
                        output.append(text)

                    i += 1

        elif line.startswith("चक्र"):

            parts = line.split()

            if len(parts) >= 2:

                count = int(parts[1])

                i += 1
                loop_block = []

                while i < len(lines) and lines[i] != "समाप्त":
                    loop_block.append(lines[i])
                    i += 1

                for n in range(count):

                    print(f"चक्र {n+1}")

                    for inner in loop_block:

                        if inner.startswith("पाठ"):
                            text = inner.replace("पाठ","").strip().strip('"')
                            print(text)
                            output.append(text)

        elif line.startswith("क्रिया"):

            name = line.replace("क्रिया","").replace(":","").strip()

            body = क्रिया_निष्पादन(name)

            for inner in body:

                if inner.startswith("पाठ"):
                    text = inner.replace("पाठ","").strip().strip('"')
                    print(text)
                    output.append(text)

        i += 1

    return output


def APK_निर्माण(name, output):

    out_dir = os.path.expanduser("~/सूत्र-तंत्र/output")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    path = os.path.join(out_dir, f"{name}.apk")

    with open(path, "w", encoding="utf-8") as f:

        f.write("Sanskrit APK\n")

        for line in output:
            f.write(line + "\n")

    print("\nAPK सफलतया संकलितम्:")
    print(path)


def निर्माण(file):

    name = os.path.basename(file).split(".")[0]

    lines = सूत्र_पढ़ें(file)

    print("सूत्र निष्पादन:")

    output = सूत्र_व्याख्या(lines)

    APK_निर्माण(name, output)
