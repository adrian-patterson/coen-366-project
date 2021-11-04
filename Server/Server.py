import socket
import threading
import time
import sys
from ClientRequests import ClientRequestHandler
from ClientDatabase import Database


class Server(threading.Thread):

    UDP_LOCALHOST_ADDRESS = "127.0.0.1"
    UDP_PORT = 8000
    BUFFER_SIZE = 1024

    def __init__(self):
        super().__init__()
        self.client_database = Database()
        self.client_list = self.client_database.open_database()
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((self.UDP_LOCALHOST_ADDRESS, self.UDP_PORT))
        print("Server Listening")

    def run(self):
        while True:
            bytes_received = self.udp_socket.recvfrom(self.BUFFER_SIZE)
            if bytes_received:
                client_request_handler = ClientRequestHandler(bytes_received, self.client_list, self.udp_socket)
                client_request_handler.start()
                client_request_handler.join()

    def exit(self):
        self.client_database.delete_database()


def main():

    server = Server()
    server.daemon = True
    server.start()

    while True:
        if input("Enter exit to quit: ") == "exit":
            server.exit()
            time.sleep(2)
            sys.exit()


if __name__ == '__main__':
    main()
