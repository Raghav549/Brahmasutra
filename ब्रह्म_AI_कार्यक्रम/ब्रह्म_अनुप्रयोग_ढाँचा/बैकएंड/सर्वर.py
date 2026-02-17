import socket
import threading


class ब्रह्मसर्वर:

    def __init__(self, host="127.0.0.1", port=8080):

        self.host = host
        self.port = port
        self.routes = {}

    def मार्ग_जोड़ो(self, path, handler):

        self.routes[path] = handler

        print(f"मार्ग जोड़ा: {path}")

    def अनुरोध_संभालो(self, client):

        data = client.recv(1024).decode("utf-8")

        if not data:

            client.close()
            return

        path = data.split(" ")[1]

        if path in self.routes:

            response = self.routes[path]

        else:

            response = "Not Found"


        http = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "\r\n"
            f"{response}"
        )


        client.send(http.encode("utf-8"))

        client.close()


    def प्रारम्भ(self):

        server = socket.socket()

        server.bind((self.host, self.port))

        server.listen(5)

        print(f"ब्रह्म सर्वर प्रारम्भ: {self.host}:{self.port}")

        while True:

            client, addr = server.accept()

            thread = threading.Thread(
                target=self.अनुरोध_संभालो,
                args=(client,)
            )

            thread.start()
