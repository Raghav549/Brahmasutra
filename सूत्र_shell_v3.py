# 🕉️ सूत्र Shell v3

import सूत्र_स्मृति_प्रबंधक as स्मृति
import सूत्र_प्रक्रिया_तंत्र as प्रक्रिया
import सूत्र_सञ्चिका_तंत्र as सञ्चिका
import सूत्र_यन्त्र_तंत्र as यन्त्र


class Shell:


    def __init__(self):

        print("🕉️ सूत्र Shell v3 सक्रिय")


    def चलाओ(self):

        while True:

            आदेश = input("सूत्र >>> ")

            if आदेश == "निर्गम":

                print("Shell बन्द")

                break


            elif आदेश == "स्मृति":

                स्मृति.प्रारम्भ()


            elif आदेश == "प्रक्रिया":

                प्रक्रिया.प्रारम्भ()


            elif आदेश == "सञ्चिका":

                सञ्चिका.प्रारम्भ()


            elif आदेश == "यन्त्र":

                यन्त्र.प्रारम्भ()


            else:

                print("अज्ञात आदेश")



def प्रारम्भ():

    shell = Shell()

    shell.चलाओ()



# auto start
प्रारम्भ()
