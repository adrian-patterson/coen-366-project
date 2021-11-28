import socket
from threading import Thread
import time
import sys
from ClientDatabase import Database
from ServerRequests import ServerRequestHandler
from Utils.UtilityFunctions import get_ip_address


class Server(Thread):
    # Server has fixed udp port and buffer size
    UDP_PORT = 5001
    BUFFER_SIZE = 4096

    def __init__(self):
        super().__init__()
        self.client_database = Database()
        self.client_list = self.client_database.open_database()
        self.ip_address = get_ip_address()
        self.udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((self.ip_address, self.UDP_PORT))
        print("Server Listening: " + str(self.udp_socket))

    def run(self):
        while True:
            bytes_received = self.udp_socket.recvfrom(self.BUFFER_SIZE)
            if bytes_received:
                server_request_handler = ServerRequestHandler(
                    bytes_received, self.client_list, self.udp_socket)
                server_request_handler.start()
                server_request_handler.join()
                self.client_list = server_request_handler.client_list


def main():
    server = Server()
    server.daemon = True
    server.start()

    while True:
        choice = input("Possible Commands:\n\n   'exit' to successfully kill server\n   'clear' to delete all "
                       "registered users\n\n")

        if choice == 'exit':
            server.client_database.delete_database()
            time.sleep(2)
            sys.exit()

        if choice == 'clear':
            server.client_list.clear()
            server.client_database.delete_database()


if __name__ == '__main__':
    main()
