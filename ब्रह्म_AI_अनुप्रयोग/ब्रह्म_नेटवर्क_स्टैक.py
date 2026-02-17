# ब्रह्म नेटवर्क स्टैक
# VERSION 56

import socket
import threading


class ब्रह्मनेटवर्कस्टैक:

    def __init__(self):

        self.connections = {}

        print("🕉️ ब्रह्म नेटवर्क स्टैक सक्रिय")


    def सर्वर_प्रारंभ(self, host="127.0.0.1", port=9090):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((host, port))

        server.listen(5)

        print(f"🕉️ ब्रह्म नेटवर्क सर्वर सक्रिय : {host}:{port}")

        threading.Thread(
            target=self._स्वीकार,
            args=(server,),
            daemon=True
        ).start()

        return {
            "status": "success",
            "port": port
        }


    def _स्वीकार(self, server):

        while True:

            client, addr = server.accept()

            self.connections[str(addr)] = client

            print(f"connection: {addr}")

            threading.Thread(
                target=self._सुनो,
                args=(client, addr),
                daemon=True
            ).start()


    def _सुनो(self, client, addr):

        while True:

            try:

                data = client.recv(1024)

                if not data:
                    break

                message = data.decode()

                print(f"message from {addr}: {message}")

                client.send(b"brahma_ack")

            except:

                break


    def भेजो(self, host, port, message):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((host, port))

        client.send(message.encode())

        response = client.recv(1024)

        client.close()

        return response.decode()
