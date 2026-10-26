# ब्रह्म प्रॉम्प्ट लोडर
# VERSION 114
# Universal Prompt Loader

import os
import urllib.error
import urllib.request

MAX_PROMPT_BYTES = 1_000_000

class ब्रह्मप्रॉम्प्टलोडर:

    def __init__(self):
        self.अंतिम_प्रॉम्प्ट = ""
        print("ब्रह्म प्रॉम्प्ट लोडर सक्रिय")

    # direct text load
    def पाठ_लोड(self, पाठ):

        if not पाठ:
            raise ValueError("प्रॉम्प्ट रिक्त है")

        self.अंतिम_प्रॉम्प्ट = str(पाठ).strip()

        print("प्रॉम्प्ट पाठ लोड सफल")

        return self.अंतिम_प्रॉम्प्ट


    # file load
    def फ़ाइल_लोड(self, पथ):

        if not os.path.exists(पथ):
            raise FileNotFoundError("फ़ाइल नहीं मिली")

        with open(पथ, "r", encoding="utf-8") as f:

            डेटा = f.read()

        self.अंतिम_प्रॉम्प्ट = डेटा.strip()

        print("प्रॉम्प्ट फ़ाइल लोड सफल")

        return self.अंतिम_प्रॉम्प्ट


    # url load (standard library only: no `requests` dependency)
    def यूआरएल_लोड(self, यूआरएल):

        if not isinstance(यूआरएल, str) or not यूआरएल.startswith(("http://", "https://")):

            raise ValueError("केवल http/https यूआरएल समर्थित है")

        try:

            with urllib.request.urlopen(यूआरएल, timeout=10) as response:

                कच्चा = response.read(MAX_PROMPT_BYTES)

                एन्कोडिंग = response.headers.get_content_charset() or "utf-8"

            self.अंतिम_प्रॉम्प्ट = कच्चा.decode(एन्कोडिंग, "replace").strip()

            print("प्रॉम्प्ट यूआरएल लोड सफल")

            return self.अंतिम_प्रॉम्प्ट

        except (urllib.error.URLError, OSError, ValueError) as e:

            raise RuntimeError(f"यूआरएल लोड विफल: {e}")


    # multi line load
    def बहुपंक्ति_लोड(self):

        print("प्रॉम्प्ट दर्ज करें (END लिखकर समाप्त करें):")

        lines = []

        while True:

            line = input()

            if line.strip() == "END":
                break

            lines.append(line)

        self.अंतिम_प्रॉम्प्ट = "\n".join(lines).strip()

        print("बहुपंक्ति प्रॉम्प्ट लोड सफल")

        return self.अंतिम_प्रॉम्प्ट


    # get prompt
    def प्राप्त(self):

        return self.अंतिम_प्रॉम्प्ट


    # clear prompt
    def साफ(self):

        self.अंतिम_प्रॉम्प्ट = ""

        print("प्रॉम्प्ट साफ किया गया")

        return True
