# 🕉️ ब्रह्म Runtime कोर
# VERSION 10

import os

from ब्रह्म_अनुप्रयोग_लोडर_कोर import ब्रह्मअनुप्रयोगलोडरकोर


print("🕉️ ब्रह्म Runtime कोर सक्रिय")


class ब्रह्मRuntimeकोर:

    def __init__(self):

        self.loader = ब्रह्मअनुप्रयोगलोडरकोर()

        self.running = False

        print("Runtime तैयार")


    def प्रारम्भ(self, अनुप्रयोग):

        print("Runtime प्रारम्भ")

        self.running = True

        self.loader.निष्पादन(अनुप्रयोग)

        print("Runtime समाप्त")

        self.running = False


    def स्थिति(self):

        if self.running:

            print("Runtime स्थिति: सक्रिय")

        else:

            print("Runtime स्थिति: निष्क्रिय")


    def रोक(self):

        print("Runtime रोक दिया गया")

        self.running = False


# test
if __name__ == "__main__":

    runtime = ब्रह्मRuntimeकोर()

    runtime.स्थिति()

    runtime.प्रारम्भ("परीक्षण.ब्रह्म")

    runtime.स्थिति()
