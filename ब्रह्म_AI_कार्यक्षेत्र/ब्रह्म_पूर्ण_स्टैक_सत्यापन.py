import socket
import urllib.request

class ब्रह्मपूर्णस्टैकसत्यापन:

    def __init__(self):
        self.backend_url = "http://127.0.0.1:5000"
        self.frontend_url = "http://127.0.0.1:8000"

    def पोर्ट_सत्यापन(self, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()

        return result == 0


    def backend_सत्यापन(self):

        try:
            response = urllib.request.urlopen(self.backend_url, timeout=3)
            return response.status == 200
        except:
            return False


    def frontend_सत्यापन(self):

        try:
            response = urllib.request.urlopen(self.frontend_url, timeout=3)
            return response.status == 200
        except:
            return False


    def पूर्ण_सत्यापन(self):

        backend_port = self.पोर्ट_सत्यापन(5000)
        frontend_port = self.पोर्ट_सत्यापन(8000)

        backend_ok = self.backend_सत्यापन()
        frontend_ok = self.frontend_सत्यापन()

        print()
        print("BRAHMA FULL STACK STATUS")
        print("------------------------")

        print("Backend Port:", "ACTIVE" if backend_port else "OFF")
        print("Frontend Port:", "ACTIVE" if frontend_port else "OFF")

        print("Backend Response:", "OK" if backend_ok else "FAIL")
        print("Frontend Response:", "OK" if frontend_ok else "FAIL")

        if backend_port and frontend_port and backend_ok and frontend_ok:

            print()
            print("BRAHMA APP FULLY LIVE")
            return True

        else:

            print()
            print("BRAHMA APP NOT FULLY LIVE")
            return False
