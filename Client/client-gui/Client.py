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
        self.udp_socket = None
        self.tcp_socket = None
        self.udp_init()
        self.tcp_init()
        print("Client Live:\t" + str(self.udp_socket) + "\n\t\t" + str(self.tcp_socket))

    def run(self):
        while True:
            # self.tcp_init()
            self.tcp_socket.listen()
            connection, address = self.tcp_socket.accept()
            try:
                while True:
                    message = connection.recv(1024)

                    if message:
                        if get_message_type(message) == "DOWNLOAD":
                            self.send_file_to_peer(message)
                    else:
                        break
            except socket.error as e:
                print("Socket Error: " + str(e))

    def udp_init(self):
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((self.ip_address, 0))
        self.udp_socket.settimeout(3)

    def tcp_init(self):
        self.tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind((self.ip_address, 0))

    def send_message_to_server(self, message):
        bytes_to_send = object_to_bytes(message)
        self.udp_socket.sendto(bytes_to_send, self.server_address)
        self.increment_rq()
        log(message)

    def connect_to_peer(self, peer_ip_address, peer_tcp_socket):
        self.tcp_socket.connect((peer_ip_address, peer_tcp_socket))
        return

    def disconnect_from_peer(self):
        self.tcp_socket.close()

    def send_message_to_peer(self, message):
        bytes_to_send = object_to_bytes(message)
        self.tcp_socket.send(bytes_to_send)
        self.increment_rq()
        log(message)

    def get_list_of_available_files(self):
        current_directory = os.getcwd()
        path = 'ClientFiles'
        os.chdir(path)
        files = os.listdir()
        for i in files:
            self.list_of_available_files.append(i)
        os.chdir(current_directory)

    def send_file_to_peer(self, download_request):
        download = Download(**bytes_to_object(download_request))
        file_name = download.file_name

        if not os.path.exists(file_name):
            download_error = DownloadError(download.rq, "File does not exist.")
            self.send_message_to_peer(download_error)
        else:
            with open(file=file_name, mode="r") as f:
                file_content = f.read()
                chunk_text = ""
                chunk_number = 0

                for character in range(0, len(file_content)):

                    if character == len(file_content) - 1:
                        chunk_text += character
                        file_end = FileEnd(download.rq, download.file_name, chunk_number, chunk_text)
                        self.send_message_to_peer(file_end)
                        break

                    elif character != 0 and (character + 1) % 200 == 0:
                        file = File(download.rq, download.file_name, chunk_number, chunk_text)
                        self.send_message_to_peer(file)
                        chunk_text = ""
                        chunk_number += 1

                    chunk_text += character
        
    def increment_rq(self):
        self.rq += 1

    def __del__(self):
        self.udp_socket.close()
