# 🕉️ सूत्र Native Binary निष्पादक


import सूत्र_यन्त्र_निष्पादक as यन्त्र


MAGIC = b"SUTRA"


class बिननिष्पादक:


    def चलाओ(self, संचिका):

        print("Binary लोड:", संचिका)


        with open(संचिका, "rb") as file:

            magic = file.read(5)

            if magic != MAGIC:

                print("अमान्य binary")
                return


            size = int.from_bytes(file.read(4), "little")

            code = file.read(size)


        temp = "temp.यन्त्र"


        with open(temp, "wb") as file:

            file.write(code)


        cpu = यन्त्र.सूत्रयन्त्र()

        cpu.चलाओ(temp)
