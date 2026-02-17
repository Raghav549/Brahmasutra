from ब्रह्म_API_निष्पादन_तंत्र import ब्रह्मAPINिष्पादनतंत्र


api = ब्रह्मAPINिष्पादनतंत्र(9100)


def test_get():

    return {
        "status": "GET working"
    }


def test_post(data):

    return {
        "status": "POST working",
        "received": data
    }


api.मार्ग_जोड़ें_GET("/test", test_get)

api.मार्ग_जोड़ें_POST("/send", test_post)

api.प्रारंभ()


input("Press Enter to exit...")
