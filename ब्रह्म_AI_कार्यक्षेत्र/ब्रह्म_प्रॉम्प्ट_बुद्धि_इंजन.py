# ब्रह्म_प्रॉम्प्ट_बुद्धि_इंजन.py
# BRAHMA UNIVERSAL PROMPT INTELLIGENCE ENGINE
# VERSION 126

class ब्रह्मप्रॉम्प्टबुद्धिइंजन:

    def __init__(self):

        print("ब्रह्म प्रॉम्प्ट बुद्धि इंजन सक्रिय")

        self.keywords = {

            "app": ["app","application","software","tool","program"],
            "website": ["website","site","web"],
            "ai": ["ai","assistant","intelligence","bot"],
            "backend": ["backend","server","api"],
            "frontend": ["frontend","ui","interface"],
            "database": ["database","db","storage"],
            "login": ["login","auth","authentication"],
            "dashboard": ["dashboard","panel"],
            "deployment": ["deploy","deployment","host"],
            "cloud": ["cloud","server"],
            "saas": ["saas","service"]

        }


    def विश्लेषण(self, prompt):

        prompt = prompt.lower()

        result = {}

        for category in self.keywords:

            result[category] = False

            for word in self.keywords[category]:

                if word in prompt:

                    result[category] = True
                    break

        return result
