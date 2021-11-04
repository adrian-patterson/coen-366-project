import json
import socket
import threading
from Utils.Registration import Register


class Client(threading.Thread):

    UDP_LOCALHOST_ADDRESS = "127.0.0.1"
    UDP_PORT = 8080
    BUFFER_SIZE = 1024
    SERVER_ADDRESS_PORT = ("127.0.0.1", 8000)

    def __init__(self):
        super().__init__()
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((self.UDP_LOCALHOST_ADDRESS, self.UDP_PORT))
        print("Client Live: " + str(self.udp_socket))

    def run(self):
        while True:
            bytes_received = self.udp_socket.recvfrom(self.BUFFER_SIZE)
            print("Message from Server: " + str(bytes_received[0]))

    def register(self):
        register = Register("Name", self.udp_socket.getsockname()[0], self.udp_socket.getsockname()[1], "TCP SOCKET")
        bytes_to_send = str.encode(json.dumps(register.__dict__))
        print(json.dumps(register.__dict__))
        self.udp_socket.sendto(bytes_to_send, self.SERVER_ADDRESS_PORT)
        print("Client message sent.")


client = Client()
client.start()
client.register()
