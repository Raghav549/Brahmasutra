print("🕉️ सूत्र कार्य निर्माता सक्रिय")

class कार्यनिर्माता:

    def निर्मित(self, input_binary, output_exec):

        with open(input_binary, "rb") as f:
            data = f.read()

        header = b"SUTRA_EXEC_V1"

        with open(output_exec, "wb") as f:

            f.write(header)
            f.write(data)

        print("कार्य निर्मित:", output_exec)
