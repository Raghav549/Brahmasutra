# 🕉️ BRAHMA CREATION BLUEPRINT ENGINE
# VERSION 110
# FULL SANSKRIT APPLICATION STRUCTURE GENERATOR

import os
import json
import uuid
import datetime

from ब्रह्म_प्रॉम्प्ट_बोध_कोर import ब्रह्मप्रॉम्प्टबोधकोर

print("🕉️ ब्रह्म निर्माण रूपरेखा कोर सक्रिय (VERSION 110)")


class ब्रह्मनिर्माणरूपरेखाकोर:

    def __init__(self):

        self.prompt_core = ब्रह्मप्रॉम्प्टबोधकोर()

        self.base_path = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/ब्रह्म_अनुप्रयोग"
        )

        os.makedirs(self.base_path, exist_ok=True)


    # मुख्य रूपरेखा निर्माण
    def रूपरेखा_निर्माण(self, prompt):

        # prompt analysis
        संरचना = self.prompt_core.बोध(prompt)

        app_name = संरचना["ऐप_नाम"]

        app_path = os.path.join(self.base_path, app_name)

        blueprint = {

            "ऐप_नाम": app_name,

            "ऐप_ID": संरचना["ID"],

            "निर्माण_समय": संरचना["निर्माण_समय"],

            "संस्करण": "110",

            "पथ": app_path,

            "घटक": संरचना["घटक"],

            "निर्देशिका": {

                "root": app_path,

                "frontend": os.path.join(app_path, "frontend"),

                "backend": os.path.join(app_path, "backend"),

                "database": os.path.join(app_path, "database"),

                "api": os.path.join(app_path, "api"),

                "assets": os.path.join(app_path, "assets"),

                "config": os.path.join(app_path, "config")

            }

        }

        return blueprint


    # directory create
    def निर्देशिका_निर्माण(self, blueprint):

        dirs = blueprint["निर्देशिका"]

        for key in dirs:

            os.makedirs(dirs[key], exist_ok=True)

        print("📁 निर्देशिका निर्मित")


    # blueprint save
    def रूपरेखा_सहेज(self, blueprint):

        config_path = os.path.join(
            blueprint["निर्देशिका"]["config"],
            "brahma_blueprint.json"
        )

        with open(config_path, "w", encoding="utf-8") as f:

            json.dump(blueprint, f, indent=4, ensure_ascii=False)

        print("💾 रूपरेखा सहेजी:", config_path)


    # full creation
    def निर्माण(self, prompt):

        blueprint = self.रूपरेखा_निर्माण(prompt)

        self.निर्देशिका_निर्माण(blueprint)

        self.रूपरेखा_सहेज(blueprint)

        print("\n🕉️ अनुप्रयोग रूपरेखा पूर्ण निर्मित")

        print("ऐप:", blueprint["ऐप_नाम"])

        print("पथ:", blueprint["पथ"])

        return blueprint


# test
if __name__ == "__main__":

    core = ब्रह्मनिर्माणरूपरेखाकोर()

    prompt = input("🕉️ प्रॉम्प्ट लिखें: ")

    blueprint = core.निर्माण(prompt)

    print("\nBlueprint:\n")

    for key in blueprint:

        print(key, ":", blueprint[key])
