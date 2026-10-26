"""API तंत्र का लघु परीक्षण।

सर्वर पृष्ठभूमि थ्रेड में चलता है। जब इसे इंटरैक्टिव रूप से चलाया जाता है तो
Enter दबाने पर बंद होता है; स्वचालित (non-tty) रूप से चलाने पर तुरंत बंद हो
जाता है, ताकि CI अटके नहीं।
"""

import sys

from ब्रह्म_API_निष्पादन_तंत्र import ब्रह्मAPIनिष्पादनतंत्र

api = ब्रह्मAPIनिष्पादनतंत्र(9100)


def test_get():
    return {"status": "GET working"}


def test_post(data):
    return {"status": "POST working", "received": data}


api.मार्ग_जोड़ें_GET("/test", test_get)
api.मार्ग_जोड़ें_POST("/send", test_post)

if __name__ == "__main__":
    api.प्रारम्भ()
    print("मार्ग: GET /test, POST /send")
    try:
        input("बंद करने के लिए Enter दबाएँ...")
    except EOFError:
        pass
    finally:
        api.बन्द()
