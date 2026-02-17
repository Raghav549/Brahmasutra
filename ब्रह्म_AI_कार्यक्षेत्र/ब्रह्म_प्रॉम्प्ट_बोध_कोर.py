# 🕉️ BRAHMA PROMPT UNDERSTANDING CORE
# VERSION 109
# FULL SANSKRIT UNIVERSAL PROMPT ANALYZER

import os
import re
import uuid
import datetime

print("🕉️ ब्रह्म प्रॉम्प्ट बोध कोर सक्रिय (VERSION 109)")


class ब्रह्मप्रॉम्प्टबोधकोर:

    def __init__(self):

        self.समर्थित_घटक = {

            "login": "प्रवेश_प्रणाली",
            "auth": "प्रमाणीकरण",
            "authentication": "प्रमाणीकरण",

            "database": "डेटाबेस",
            "db": "डेटाबेस",

            "api": "API",
            "backend": "बैकएंड",

            "frontend": "फ्रंटएंड",
            "ui": "फ्रंटएंड",

            "dashboard": "डैशबोर्ड",
            "admin": "प्रशासन",

            "chat": "संदेश_प्रणाली",
            "message": "संदेश_प्रणाली",

            "payment": "भुगतान",
            "subscription": "सदस्यता",

            "upload": "अपलोड",
            "download": "डाउनलोड",

            "profile": "प्रोफ़ाइल",

            "search": "खोज",

            "notification": "सूचना"

        }

        self.समर्थित_ऐप_प्रकार = {

            "chat": "chat_app",
            "social": "social_app",
            "ecommerce": "ecommerce_app",
            "store": "store_app",
            "dashboard": "dashboard_app",
            "admin": "admin_app",
            "ai": "ai_app",
            "tool": "tool_app",
            "website": "website",
            "saas": "saas_app"

        }


    # प्रॉम्प्ट सामान्यीकरण
    def सामान्यीकृत(self, prompt):

        prompt = prompt.lower()
        prompt = prompt.strip()

        return prompt


    # ऐप नाम पहचान
    def ऐप_नाम_पहचान(self, prompt):

        for key in self.समर्थित_ऐप_प्रकार:

            if key in prompt:

                return self.समर्थित_ऐप_प्रकार[key]

        # fallback auto name
        unique = str(uuid.uuid4()).replace("-", "")[:8]

        return "brahma_app_" + unique


    # घटक पहचान
    def घटक_पहचान(self, prompt):

        घटक = []

        for key in self.समर्थित_घटक:

            if key in prompt:

                घटक.append(self.समर्थित_घटक[key])

        # default components always added

        if "फ्रंटएंड" not in घटक:
            घटक.append("फ्रंटएंड")

        if "बैकएंड" not in घटक:
            घटक.append("बैकएंड")

        if "डेटाबेस" not in घटक:
            घटक.append("डेटाबेस")

        return list(set(घटक))


    # संरचना निर्माण
    def संरचना_निर्माण(self, ऐप_नाम, घटक, prompt):

        संरचना = {

            "ऐप_नाम": ऐप_नाम,

            "घटक": घटक,

            "प्रॉम्प्ट": prompt,

            "निर्माण_समय": str(datetime.datetime.now()),

            "संस्करण": "109",

            "ID": str(uuid.uuid4())

        }

        return संरचना


    # मुख्य बोध प्रणाली
    def बोध(self, prompt):

        prompt = self.सामान्यीकृत(prompt)

        ऐप_नाम = self.ऐप_नाम_पहचान(prompt)

        घटक = self.घटक_पहचान(prompt)

        संरचना = self.संरचना_निर्माण(ऐप_नाम, घटक, prompt)

        return संरचना


# परीक्षण
if __name__ == "__main__":

    core = ब्रह्मप्रॉम्प्टबोधकोर()

    prompt = input("🕉️ प्रॉम्प्ट लिखें: ")

    result = core.बोध(prompt)

    print("\n🕉️ विश्लेषण परिणाम:\n")

    for key in result:

        print(f"{key} : {result[key]}")
