# सूत्र तंत्र — Machine Language Builder

print("सूत्र Machine Builder आरम्भ")



# instruction encoding
encoding = {
    "लोड": "01",
    "योग": "02",
    "गुण": "03",
    "दर्शय": "04"
}



# convert to machine code
def bin_निर्माण(input_file, output_file):

    with open(input_file, encoding="utf-8") as f:

        lines = f.readlines()


    output = []


    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue


        cmd = parts[0]


        if cmd in encoding:

            code = encoding[cmd]

            args = " ".join(parts[1:])

            output.append(code + " " + args)


    with open(output_file, "w", encoding="utf-8") as f:

        for line in output:

            f.write(line + "\n")


    print("Machine file निर्मित:", output_file)



# start
if __name__ == "__main__":

    bin_निर्माण("cpu.sutra", "cpu.सूत्रbin")
