import os
from threading import Thread
from Utils.FileTransfer import File, DownloadError, Download, FileEnd
from Utils.UtilityFunctions import *

BUFFER_SIZE = 4096


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
        self.udp_socket = self.udp_init(0)
        self.tcp_socket = self.tcp_init(0)
        print("Client Live:\n\t\tUDP:\t" + str(self.udp_socket) +
              "\n\t\tTCP:\t" + str(self.tcp_socket))

    def run(self):
        self.tcp_socket.listen()

        while True:
            peer_socket = self.tcp_socket.accept()[0]
            peer_handler = Thread(
                target=self.handle_peer_request, args=(peer_socket,))
            peer_handler.start()

    def udp_init(self, port):
        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind((self.ip_address, port))
        udp_socket.settimeout(3)
        return udp_socket

    def tcp_init(self, port):
        tcp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((self.ip_address, port))
        return tcp_socket

    def handle_peer_request(self, peer_socket):
        try:
            while True:
                bytes_received = peer_socket.recv(BUFFER_SIZE)

                if bytes_received:
                    if get_message_type(bytes_received) == "DOWNLOAD":
                        self.send_file_to_peer(bytes_received, peer_socket)
                else:
                    break

        except socket.error as e:
            print("Socket Error: " + str(e))

        peer_socket.close()

    def send_file_to_peer(self, bytes_received, peer_socket):
        download = Download(**bytes_to_object(bytes_received))
        file_name = download.file_name
        path_to_file = os.getcwd() + "/ClientFiles/" + file_name

        if not os.path.exists(path_to_file):
            download_error = DownloadError(download.rq, "File does not exist.")
            self.send_message_to_peer(download_error, peer_socket)
        else:
            with open(file=path_to_file, mode="r") as f:
                file_content = f.read()
                if file_content == "":
                    file_end = FileEnd(
                        download.rq, download.file_name, 0, "")
                    self.send_message_to_peer(file_end, peer_socket)
                    return

                chunk_text = ""
                chunk_number = 0

                for character in range(0, len(file_content)):
                    if character == len(file_content) - 1:
                        chunk_text += file_content[character]
                        file_end = FileEnd(
                            download.rq, download.file_name, chunk_number, chunk_text)
                        self.send_message_to_peer(file_end, peer_socket)
                        break
                    elif character != 0 and (character + 1) % 200 == 0:
                        file = File(download.rq, download.file_name,
                                    chunk_number, chunk_text)
                        self.send_message_to_peer(file, peer_socket)
                        chunk_text = ""
                        chunk_number += 1
                    chunk_text += file_content[character]

    def send_message_to_server(self, message):
        bytes_to_send = object_to_bytes(message)
        self.udp_socket.sendto(bytes_to_send, self.server_address)
        self.increment_rq()
        log(message)

    def send_message_to_peer(self, message, peer_socket):
        bytes_to_send = object_to_bytes(message)
        peer_socket.send(bytes_to_send)
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

    def increment_rq(self):
        self.rq += 1

    def __del__(self):
        self.udp_socket.close()
