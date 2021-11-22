import os
from threading import Thread
from Utils.FileTransfer import File, DownloadError, Download, FileEnd
from Utils.UtilityFunctions import *

BUFFER_SIZE = 1024


class Client(Thread):

    SERVER_UDP_PORT = 5001

    def __init__(self):
        super().__init__()
        self.rq = 0
        self.name = ""
        self.list_of_available_files = []
        self.get_list_of_available_files()
        self.ip_address = get_ip_address()
        self.server_address = None
        self.udp_socket = self.udp_init()
        self.tcp_socket = self.tcp_init()
        print("Client Live:\n\t\tUDP:\t" + str(self.udp_socket) +
              "\n\t\tTCP:\t" + str(self.tcp_socket))

    def run(self):
        self.tcp_socket.listen()

        while True:
            client_socket, client_address = self.tcp_socket.accept()
            print("Peer Connected: " + str(client_address[1]))
            peer_handler = Thread(
                target=self.handle_peer_request, args=(client_socket,))
            peer_handler.start()

    def udp_init(self):
        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind((self.ip_address, 0))
        udp_socket.settimeout(3)
        return udp_socket

    def tcp_init(self):
        tcp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((self.ip_address, 0))
        return tcp_socket

    def handle_peer_request(self, client_socket):
        try:
            while True:
                bytes_received = client_socket.recv(1024)

                if bytes_received:
                    if get_message_type(bytes_received) == "DOWNLOAD":
                        self.send_file_to_peer(bytes_received, client_socket)
                else:
                    break

        except socket.error as e:
            print("Socket Error: " + str(e))

        client_socket.close()

    def send_file_to_peer(self, bytes_received, client_socket):
        download = Download(**bytes_to_object(bytes_received))
        file_name = download.file_name
        path_to_file = os.getcwd() + "/ClientFiles/" + file_name

        if not os.path.exists(path_to_file):
            download_error = DownloadError(download.rq, "File does not exist.")
            print(download_error)
            # TODO: send back download denied

        else:
            with open(file=path_to_file, mode="r") as f:
                file_content = f.read()
                chunk_text = ""
                chunk_number = 0

                for character in range(0, len(file_content)):

                    if character == len(file_content) - 1:
                        chunk_text += file_content[character]
                        file_end = FileEnd(
                            download.rq, download.file_name, chunk_number, chunk_text)
                        self.send_message_to_peer(file_end, client_socket)
                        log(file)
                        break

                    elif character != 0 and (character + 1) % 200 == 0:
                        file = File(download.rq, download.file_name,
                                    chunk_number, chunk_text)
                        self.send_message_to_peer(file, client_socket)
                        chunk_text = ""
                        chunk_number += 1
                        log(file)

                    chunk_text += file_content[character]

    def send_message_to_server(self, message):
        bytes_to_send = object_to_bytes(message)
        self.udp_socket.sendto(bytes_to_send, self.server_address)
        self.increment_rq()
        log(message)

    def send_message_to_peer(self, message, client_socket):
        bytes_to_send = object_to_bytes(message)
        client_socket.send(bytes_to_send)
        self.increment_rq()
        log(message)

    def connect_to_peer(self, peer_ip_address, peer_tcp_socket):
        self.tcp_socket.connect((peer_ip_address, peer_tcp_socket))
        return

    def get_list_of_available_files(self):
        current_directory = os.getcwd()
        path = 'ClientFiles'
        os.chdir(path)
        files = os.listdir()
        for i in files:
            self.list_of_available_files.append(i)
        os.chdir(current_directory)

    def increment_rq(self):
        self.rq += 1

    def __del__(self):
        self.udp_socket.close()
