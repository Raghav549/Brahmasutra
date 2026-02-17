# ब्रह्म_स्वायत्त_अनुप्रयोग_जनक.py
# BRAHMA Autonomous App Generator Core
# VERSION 125

import os
import time
from ब्रह्म_पूर्ण_स्टैक_जनक import ब्रह्मपूर्णस्टैकजनक

class ब्रह्मस्वायत्तअनुप्रयोगजनक:

    def __init__(self, workspace):

        self.workspace = workspace

        print("ब्रह्म स्वायत्त अनुप्रयोग जनक सक्रिय")


    def नाम_निर्माण(self, prompt):

        name = prompt.lower()

        name = name.replace("create","")
        name = name.replace("build","")
        name = name.replace("generate","")
        name = name.replace("app","")
        name = name.replace("application","")

        name = name.strip().replace(" ","_")

        if name == "":
            name = "brahma_app_" + str(int(time.time()))

        return name


    def अनुप्रयोग_निर्माण(self, prompt):

        print("प्रॉम्प्ट विश्लेषण प्रारंभ")

        app_name = self.नाम_निर्माण(prompt)

        print("अनुप्रयोग नाम:", app_name)

        generator = ब्रह्मपूर्णस्टैकजनक(self.workspace)

        generator.जनन(app_name)

        print("पूर्ण अनुप्रयोग निर्माण सफल")

        return app_name
