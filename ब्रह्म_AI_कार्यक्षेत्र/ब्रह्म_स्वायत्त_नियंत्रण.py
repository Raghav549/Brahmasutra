# ब्रह्म स्वायत्त नियंत्रण तंत्र
# Version 102

import os
import time

from ब्रह्म_तैनाती_इंजन import ब्रह्मतैनातीइंजन


class ब्रह्मस्वायत्तनियंत्रण:

    def __init__(self, कार्यक्षेत्र):
        self.कार्यक्षेत्र = कार्यक्षेत्र
        self.इंजन = ब्रह्मतैनातीइंजन()
        self.ज्ञात_अनुप्रयोग = set()

        print("ब्रह्म स्वायत्त नियंत्रण सक्रिय")


    def स्कैन(self):

        files = os.listdir(self.कार्यक्षेत्र)

        for file in files:

            if file.endswith(".py"):

                full_path = os.path.join(self.कार्यक्षेत्र, file)

                if full_path not in self.ज्ञात_अनुप्रयोग:

                    print("नया अनुप्रयोग मिला:", file)

                    try:

                        self.इंजन.तैनात(full_path)

                        self.ज्ञात_अनुप्रयोग.add(full_path)

                        print("स्वतः तैनात:", file)

                    except Exception as e:

                        print("त्रुटि:", e)


    def प्रारंभ(self):

        print("स्वायत्त निगरानी प्रारंभ")

        while True:

            self.स्कैन()

            time.sleep(3)
