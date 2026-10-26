

# --- headless-safe input -----------------------------------------------------
# These demos read from a terminal.  Under CI, `nohup` or the legacy baseline
# there is no terminal, and a raw `input()` raises EOFError (exit 1) or spins.
# `_इनपुट` behaves like `input()` interactively and stops cleanly otherwise.
_EOF_गिनती = {"n": 0}


def _इनपुट(prompt=""):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        _EOF_गिनती["n"] += 1
        if _EOF_गिनती["n"] > 1:
            raise SystemExit(0)
        return "निर्गम"

# 🕉️ BRAHMA CREATION BLUEPRINT ENGINE
# VERSION 110
# FULL SANSKRIT APPLICATION STRUCTURE GENERATOR

import os
import json
import uuid
import datetime

from ब्रह्म_प्रॉम्प्ट_बोध_कोर import ब्रह्मप्रॉम्प्टबोधकोर


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


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global blueprint, core, key, prompt

    print("🕉️ ब्रह्म निर्माण रूपरेखा कोर सक्रिय (VERSION 110)")
    core = ब्रह्मनिर्माणरूपरेखाकोर()

    prompt = _इनपुट("🕉️ प्रॉम्प्ट लिखें: ")

    blueprint = core.निर्माण(prompt)

    print("\nBlueprint:\n")

    for key in blueprint:

        print(key, ":", blueprint[key])


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
