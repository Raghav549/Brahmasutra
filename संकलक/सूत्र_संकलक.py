# 🕉️ सूत्र संकलक

class सूत्रसंकलक:

    def __init__(self):

        print("🕉️ सूत्र संकलक सक्रिय")


    def संकलन(self, स्रोत, लक्ष्य):

        print("संकलन प्रारम्भ")

        with open(स्रोत,"r",encoding="utf-8") as f:

            पंक्तियाँ = f.readlines()


        द्विआधारी = []


        for पंक्ति in पंक्तियाँ:

            पंक्ति = पंक्ति.strip()

            if पंक्ति == "":

                continue


            भाग = पंक्ति.split()


            आदेश = भाग[0]


            if आदेश == "संकल्प":

                द्विआधारी.append({

                    "opcode":"LOAD",
                    "op1":भाग[1],
                    "op2":int(भाग[2])

                })


            elif आदेश == "योग":

                द्विआधारी.append({

                    "opcode":"ADD",
                    "op1":भाग[1],
                    "op2":भाग[2]

                })


            elif आदेश == "दर्शय":

                द्विआधारी.append({

                    "opcode":"SHOW",
                    "op1":भाग[1]

                })


            elif आदेश == "निर्गम":

                द्विआधारी.append({

                    "opcode":"EXIT"

                })


        with open(लक्ष्य,"w",encoding="utf-8") as f:

            f.write(str(द्विआधारी))


        print("संकलन पूर्ण:", लक्ष्य)
