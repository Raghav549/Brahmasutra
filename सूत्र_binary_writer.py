# 🕉️ सूत्र Binary Writer

class सूत्रBinaryWriter:

    def __init__(self):

        print("🕉️ सूत्र Binary Writer सक्रिय")


    def write(self, machine_code, filename):

        with open(filename, "wb") as f:

            for instr in machine_code:

                for item in instr:

                    if isinstance(item, int):

                        f.write(item.to_bytes(4, "little"))

                    elif isinstance(item, str):

                        data = item.encode("utf-8")

                        length = len(data)

                        f.write(length.to_bytes(4,"little"))

                        f.write(data)


        print("Binary निर्मित:", filename)
