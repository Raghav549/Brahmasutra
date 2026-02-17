# ब्रह्म नेटवर्क तंत्र

import urllib.request
import urllib.parse


class ब्रह्मनेटवर्कतंत्र:

    def __init__(self):

        print("🕉️ ब्रह्म नेटवर्क तंत्र सक्रिय")


    def प्राप्त(self, url):

        try:

            with urllib.request.urlopen(url) as response:

                data = response.read()

                return data.decode()

        except Exception as e:

            return f"त्रुटि: {e}"


    def भेजें(self, url, data):

        try:

            encoded = urllib.parse.urlencode(data).encode()

            req = urllib.request.Request(url, data=encoded)

            with urllib.request.urlopen(req) as response:

                result = response.read()

                return result.decode()

        except Exception as e:

            return f"त्रुटि: {e}"


    def परीक्षण(self):

        print("नेटवर्क परीक्षण...")

        result = self.प्राप्त("http://example.com")

        if result:
            print("नेटवर्क कार्यरत")
        else:
            print("नेटवर्क विफल")
