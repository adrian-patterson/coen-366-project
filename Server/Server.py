import socket
import threading
from ClientRequests import ClientRequestHandler
from Utils.ClientDatabase import Database


class Server(threading.Thread):
    UDP_LOCALHOST_ADDRESS = "127.0.0.1"
    UDP_PORT = 8000
    BUFFER_SIZE = 1024

    def __init__(self):
        super().__init__()
        self.client_list = []
        self.client_database = Database()
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((self.UDP_LOCALHOST_ADDRESS, self.UDP_PORT))
        print("Server Listening")

    def run(self):
        while True:
            bytes_received = self.udp_socket.recvfrom(self.BUFFER_SIZE)
            if bytes_received:
                client_request_handler = ClientRequestHandler(bytes_received, self.client_list)
                client_request_handler.start()
                client_request_handler.join()


def main():

    server = Server()

    try:
        server.start()
    finally:
        client_database = Database()
        client_database.delete_database()


if __name__ == '__main__':
    main()
