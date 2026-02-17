# 🕉️ सूत्र Native Binary संकलक


class Nativeसंकलक:


    HEADER = [83, 85, 84, 82, 65]   # "SUTRA" signature


    def compile(self, bytecode_file, output_file):

        with open(bytecode_file, "rb") as f:

            bytecode = list(f.read())


        binary = []


        # add header
        binary.extend(self.HEADER)


        # convert bytecode → native instruction format

        i = 0

        while i < len(bytecode):

            opcode = bytecode[i]


            if opcode == 1:  # चर_निर्माण

                reg = bytecode[i+1]
                val = bytecode[i+2]

                binary.extend([10, reg, val])

                i += 3


            elif opcode == 2:  # योग

                r1 = bytecode[i+1]
                r2 = bytecode[i+2]

                binary.extend([20, r1, r2])

                i += 3


            elif opcode == 3:  # दर्शय

                reg = bytecode[i+1]

                binary.extend([30, reg])

                i += 2


            elif opcode == 4:  # निर्गम

                binary.append(255)

                i += 1


            else:

                i += 1


        with open(output_file, "wb") as f:

            f.write(bytes(binary))


        print("🕉️ Native Binary निर्मित:", output_file)
