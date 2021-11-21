import os
from threading import Thread
from Utils.FileTransfer import File, DownloadError, Download, FileEnd
from Utils.Registration import Register
from Utils.UtilityFunctions import *
from Utils.Publishing import Publish, Published, PublishDenied, Remove, RemoveDenied, Removed
from Utils.Retrieve import RetrieveAll, Retrieve, RetrieveError, RetrieveInfoRequest, RetrieveInfoResponse, SearchError, SearchFileRequest, SearchFileResponse
from Utils.UpdateInformation import UpdateDenied, UpdateConfirmed, UpdateContact

BUFFER_SIZE = 1024


class Client(Thread):
    UDP_PORT = 5003
    TCP_PORT = 5004
    SERVER_UDP_PORT = 8080

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
        self.udp_socket.bind((self.ip_address, self.UDP_PORT))
        self.udp_socket.settimeout(3)

    def tcp_init(self):
        self.tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind((self.ip_address, self.TCP_PORT))

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


class RegisterWithServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.server_response = None
        self.result = None
        self.response_messages = {
            "REGISTERED": self.registered,
            "REGISTER-DENIED": self.register_denied
        }

    def run(self):
        register = Register(self.client.rq, self.client.name, self.client.ip_address, self.client.udp_socket.getsockname()[1],
                            "TCP SOCKET")
        self.client.send_message_to_server(register)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection to Server timed out."

    def join(self, *args, **kwargs):
        super().join()
        return self.result


    def increment_rq(self):
        self.rq += 1

    def __del__(self):
        self.udp_socket.close()

    def run(self):
        publish = Publish(self.client.rq, self.client.name, self.list_of_files_to_publish)
        self.client.send_message_to_server(publish)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def published(self):
        published = Published(**bytes_to_object(self.server_response[0]))
        log(published)
        return True

    def publish_denied(self):
        publish_denied = PublishDenied(**bytes_to_object(self.server_response[0]))
        log(publish_denied)
        return publish_denied.reason


class RemoveFilesFromServer(Thread):
    def __init__(self, client, list_of_files_to_remove):
        super().__init__()
        self.client = client
        self.list_of_files_to_remove = list_of_files_to_remove
        self.server_response = None
        self.result = None
        self.response_messages = {
            "REMOVED": self.removed,
            "REMOVE-DENIED": self.remove_denied
        }

    def run(self):
        remove = Remove(self.client.rq, self.client.name, self.list_of_files_to_remove)
        self.client.send_message_to_server(remove)
        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def removed(self):
        removed = Removed(**bytes_to_object(self.server_response[0]))
        log(removed)
        return True

    def remove_denied(self):
        remove_denied = RemoveDenied(**bytes_to_object(self.server_response[0]))
        log(remove_denied)
        return remove_denied.reason
