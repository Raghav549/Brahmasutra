# सूत्र तंत्र — सूत्र Executable Builder

print("सूत्र executable निर्माता सक्रिय")



HEADER = "सूत्रEXEC"



def executable_बनाओ(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:

        code = f.read()


    with open(output_file, "w", encoding="utf-8") as f:

        f.write(HEADER + "\n")

        f.write(code)


    print("Executable निर्मित:", output_file)



if __name__ == "__main__":

    executable_बनाओ("program.sbc", "program.सूत्र")
