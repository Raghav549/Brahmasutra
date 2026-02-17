# ब्रह्म प्रॉम्प्ट विश्लेषक
# VERSION 115
# Universal Prompt Analyzer Engine

import re
import json

class ब्रह्मप्रॉम्प्टविश्लेषक:

    def __init__(self):

        self.विश्लेषण = {}

        print("ब्रह्म प्रॉम्प्ट विश्लेषक सक्रिय")


    def विश्लेषण_कर(self, प्रॉम्प्ट):

        प्रॉम्प्ट = प्रॉम्प्ट.lower()

        self.विश्लेषण = {

            "app": False,
            "website": False,
            "ai": False,
            "saas": False,
            "backend": False,
            "frontend": False,
            "database": False,
            "login": False,
            "dashboard": False,
            "api": False,
            "cloud": False,
            "deployment": False,
            "mobile": False,
            "desktop": False,
            "os": False

        }

        keywords = {

            "app": ["app", "application"],
            "website": ["website", "site"],
            "ai": ["ai", "artificial intelligence"],
            "saas": ["saas"],
            "backend": ["backend", "server"],
            "frontend": ["frontend", "ui"],
            "database": ["database", "db"],
            "login": ["login", "auth"],
            "dashboard": ["dashboard"],
            "api": ["api"],
            "cloud": ["cloud"],
            "deployment": ["deploy", "deployment"],
            "mobile": ["mobile", "android"],
            "desktop": ["desktop"],
            "os": ["os", "operating system"]

        }

        for key, words in keywords.items():

            for word in words:

                if word in प्रॉम्प्ट:

                    self.विश्लेषण[key] = True


        # complexity score
        score = sum(self.विश्लेषण.values())

        if score <= 3:
            level = "basic"
        elif score <= 7:
            level = "advanced"
        else:
            level = "god-level"

        self.विश्लेषण["complexity"] = level

        print("प्रॉम्प्ट विश्लेषण पूर्ण")

        return self.विश्लेषण


    def प्राप्त(self):

        return self.विश्लेषण


    def json(self):

        return json.dumps(self.विश्लेषण, indent=4)
