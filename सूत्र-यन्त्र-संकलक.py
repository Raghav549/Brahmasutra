# =========================================
# सूत्र स्वदेशी यन्त्र-कोड संकलक
# =========================================

import struct


print("🕉️ सूत्र यन्त्र संकलक सक्रिय")


opcode = {

    "स्थापय": 1,
    "योग": 2,
    "घटा": 3,
    "गुण": 4,
    "दर्शय": 5

}


register_map = {

    "अ": 1,
    "ब": 2,
    "स": 3,
    "द": 4

}


def संकलन(इनपुट, आउटपुट):

    with open(इनपुट, "r", encoding="utf-8") as f:

        पंक्तियाँ = f.readlines()


    with open(आउटपुट, "wb") as f:

        for पंक्ति in पंक्तियाँ:

            भाग = पंक्ति.strip().split()

            if len(भाग) == 0:
                continue


            आदेश = भाग[0]

            op = opcode.get(आदेश, 0)


            if आदेश == "स्थापय":

                reg = register_map.get(भाग[1], 0)

                val = int(भाग[2])

                f.write(struct.pack("B B I", op, reg, val))


            elif आदेश in ["योग", "घटा", "गुण"]:

                reg1 = register_map.get(भाग[1], 0)

                reg2 = register_map.get(भाग[2], 0)

                f.write(struct.pack("B B B", op, reg1, reg2))


            elif आदेश == "दर्शय":

                reg = register_map.get(भाग[1], 0)

                f.write(struct.pack("B B", op, reg))


    print("संकलन पूर्ण:", आउटपुट)


इनपुट = input("सूत्र संचिका: ")

आउटपुट = input("यन्त्र संचिका: ")

संकलन(इनपुट, आउटपुट)
