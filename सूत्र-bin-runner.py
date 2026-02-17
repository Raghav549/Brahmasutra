# सूत्र तंत्र — Machine Executor

print("सूत्र Machine Runner आरम्भ")



# registers
reg = {
    "अ": 0,
    "ब": 0
}



# decode
decode = {
    "01": "लोड",
    "02": "योग",
    "03": "गुण",
    "04": "दर्शय"
}



def run(file):

    with open(file, encoding="utf-8") as f:

        lines = f.readlines()


    for line in lines:

        parts = line.strip().split()

        code = parts[0]


        cmd = decode[code]


        if cmd == "लोड":

            reg[parts[1]] = int(parts[2])

            print("लोड:", parts[1], reg[parts[1]])


        elif cmd == "योग":

            reg[parts[1]] += reg[parts[2]]

            print("योग:", reg[parts[1]])


        elif cmd == "गुण":

            reg[parts[1]] *= reg[parts[2]]

            print("गुण:", reg[parts[1]])


        elif cmd == "दर्शय":

            print("मान:", reg[parts[1]])



# start
if __name__ == "__main__":

    run("cpu.सूत्रbin")
