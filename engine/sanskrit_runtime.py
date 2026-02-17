# संस्कृत Runtime Engine with Function Support

variables = {}
functions = {}

# देवनागरी संख्या conversion
def संख्या_परिवर्तन(text):

    mapping = {
        "०":"0","१":"1","२":"2","३":"3","४":"4",
        "५":"5","६":"6","७":"7","८":"8","९":"9"
    }

    for k,v in mapping.items():
        text = text.replace(k,v)

    return text


# function execute
def कार्य_चलाओ(name):

    if name in functions:

        for line in functions[name]:

            if line.startswith("पाठ "):

                text = line.replace("पाठ ", "").replace('"',"")
                print(text)


# main runtime
def चलाओ(file):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # define function
        if line.startswith("कार्य ") and line.endswith(":"):

            fname = line.replace("कार्य ", "").replace(":", "")
            functions[fname] = []

            i += 1

            while lines[i].strip() != "समाप्त":

                functions[fname].append(lines[i].strip())
                i += 1


        # call function
        elif line.startswith("चलाओ "):

            fname = line.replace("चलाओ ", "")
            कार्य_चलाओ(fname)


        # variable
        elif line.startswith("चर "):

            parts = line.replace("चर ", "").split("=")

            name = parts[0].strip()
            value = संख्या_परिवर्तन(parts[1].strip())

            try:
                value = int(value)
            except:
                value = value.replace('"',"")
            
            variables[name] = value


        # print
        elif line.startswith("पाठ "):

            text = line.replace("पाठ ", "").strip()

            if text.startswith('"') and text.endswith('"'):
                print(text.replace('"',""))

            elif text in variables:
                print(variables[text])


        # loop
        elif line.startswith("चक्र "):

            count = line.replace("चक्र ", "").replace(":", "")
            count = संख्या_परिवर्तन(count)

            count = int(count)

            i += 1
            nextline = lines[i].strip()

            for x in range(count):

                if nextline.startswith("पाठ "):

                    text = nextline.replace("पाठ ", "").replace('"',"")
                    print(text)


        i += 1
