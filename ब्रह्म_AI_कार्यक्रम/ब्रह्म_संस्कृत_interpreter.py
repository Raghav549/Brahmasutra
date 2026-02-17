import os


class ब्रह्मसंस्कृतInterpreter:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत Interpreter V90 सक्रिय")

        self.memory = {}

        self.functions = {}

        self.modules = {}

        self.library_path = "पुस्तकालय"



    def parse(self, code):

        lines = code.split("\n")

        return [line.strip() for line in lines if line.strip()]



    def get_value(self, name):

        if name.isdigit():

            return int(name)

        return int(self.memory.get(name, 0))



    def load_module(self, name):

        if "." in name:

            parts = name.split(".")

            path = os.path.join(self.library_path, *parts) + ".ब्रह्म"

        else:

            path = name + ".ब्रह्म"



        if os.path.exists(path):

            with open(path, "r", encoding="utf-8") as f:

                code = f.read()

                self.modules[name] = code

                print("पैकेज आयात:", name)

                self.execute(code)

        else:

            print("पैकेज नहीं मिला:", name)



    def execute(self, code):

        lines = self.parse(code)

        i = 0

        while i < len(lines):

            line = lines[i]



            if line.startswith("आयात"):

                module = line.replace("आयात", "").strip()

                self.load_module(module)



            elif line.startswith("कार्य"):

                fname = line.replace("कार्य", "").strip()

                buffer = []

                i += 1

                while i < len(lines) and lines[i] != "समाप्त":

                    buffer.append(lines[i])

                    i += 1

                self.functions[fname] = buffer



            elif line.startswith("चलाओ"):

                fname = line.replace("चलाओ", "").strip()

                if fname in self.functions:

                    for fline in self.functions[fname]:

                        self.execute_line(fline)



            else:

                self.execute_line(line)



            i += 1



    def execute_line(self, line):



        if line.startswith("दर्शय"):

            key = line.replace("दर्शय", "").strip()

            print(self.memory.get(key, key))

            return



        if line.startswith("स्मृति"):

            parts = line.split("=")

            key = parts[0].replace("स्मृति", "").strip()

            value = parts[1].strip()

            self.memory[key] = value

            return



        if line.startswith("जोड़"):

            parts = line.replace("जोड़", "").strip().split("=")

            dest = parts[0].strip()

            a, b = parts[1].strip().split()

            self.memory[dest] = self.get_value(a) + self.get_value(b)

            return



        if line.startswith("सञ्चिका_लिख"):

            parts = line.replace("सञ्चिका_लिख", "").strip().split()

            filename = parts[0]

            content = " ".join(parts[1:])

            with open(filename, "w", encoding="utf-8") as f:

                f.write(content)

            print("सञ्चिका लिखित:", filename)

            return



        if line.startswith("सञ्चिका_पठ"):

            filename = line.replace("सञ्चिका_पठ", "").strip()

            if os.path.exists(filename):

                with open(filename, "r", encoding="utf-8") as f:

                    print(f.read())

            else:

                print("सञ्चिका नहीं मिली")

            return



        print("अज्ञात आदेश:", line)
