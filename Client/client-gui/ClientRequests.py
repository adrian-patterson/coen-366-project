import socket
from threading import Thread
from Client import Client
from Utils.FileTransfer import Download, File, FileEnd, DownloadError
from Utils.Publishing import Publish, Published, PublishDenied, Remove, Removed, RemoveDenied
from Utils.Registration import Register, Registered, RegisterDenied, DeRegister
from Utils.Retrieve import Retrieve, RetrieveAll, RetrieveError, RetrieveInfoRequest, RetrieveInfoResponse, SearchError, SearchFileRequest, SearchFileResponse
from Utils.UpdateInformation import UpdateConfirmed, UpdateContact, UpdateDenied
from Utils.UtilityFunctions import bytes_to_object, log, get_message_type

BUFFER_SIZE = 1024


class RegisterWithServer(Thread):

    def __init__(self, client, server_ip_address):
        super().__init__()
        self.client = client
        self.client.server_address = (server_ip_address, self.client.SERVER_UDP_PORT)
        self.server_response = None
        self.result = None
        self.response_messages = {
            "REGISTERED": self.registered,
            "REGISTER-DENIED": self.register_denied
        }

    def run(self):
        register = Register(self.client.rq, 
                            self.client.name, self.client.ip_address,
                            self.client.udp_socket.getsockname()[1],
                            self.client.tcp_socket.getsockname()[1])
        self.client.send_message_to_server(register)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()

        except socket.error:
            self.result = "Connection to Server timed out."

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def registered(self):
        registered = Registered(**bytes_to_object(self.server_response[0]))
        log(registered)
        return True

    def register_denied(self):
        register_denied = RegisterDenied(**bytes_to_object(self.server_response[0]))
        log(register_denied)
        return register_denied.reason


class DeRegisterFromServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        de_register = DeRegister(self.client.rq, self.client.name)
        self.client.send_message_to_server(de_register)
        log(de_register)


class PublishFilesToServer(Thread):

    def __init__(self, client, list_of_files_to_publish):
        super().__init__()
        self.client = client
        self.server_response = None
        self.list_of_files_to_publish = list_of_files_to_publish
        self.result = None
        self.response_messages = {
            "PUBLISHED": self.published,
            "PUBLISH-DENIED": self.publish_denied
        }

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


class RetrieveAllClientsFromServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.server_response = None
        self.result = None
        self.response_messages = {
            "RETRIEVE": self.retrieve,
            "RETRIEVE_ERROR": self.retrieve_error
        }

    def run(self):
        retrieve_all = RetrieveAll(self.client.rq)
        self.client.send_message_to_server(retrieve_all)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def retrieve(self):
        retrieve = Retrieve(**bytes_to_object(self.server_response[0]))
        log(retrieve)
        return True

    def retrieve_error(self):
        retrieve_error = RetrieveError(**bytes_to_object(self.server_response[0]))
        log(retrieve_error)
        return retrieve_error.reason


class RetrieveClientInfoFromServer(Thread):

    def __init__(self, client, name):
        super().__init__()
        self.client = client
        self.server_response = None
        self.name = name
        self.result = None
        self.response_messages = {
            "RETRIEVE-INFOT": self.retrieve_infot,
            "RETRIEVE-ERROR": self.retrieve_error
        }

    def run(self):
        retrieve_info_request = RetrieveInfoRequest(self.client.rq, self.name)
        self.client.send_message_to_server(retrieve_info_request)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def retrieve_infot(self):
        retrieve_info_response = RetrieveInfoResponse(**bytes_to_object(self.server_response[0]))
        log(retrieve_info_response)
        return True

    def retrieve_error(self):
        retrieve_error = RetrieveError(**bytes_to_object(self.server_response[0]))
        log(retrieve_error)
        return retrieve_error.reason


class SearchFileFromDataBase(Thread):

    def __init__(self, client, file_name):
        super().__init__()
        self.client = client
        self.server_response = None
        self.file_name = file_name
        self.result = None
        self.response_messages = {
            "SEARCH-FILE": self.search_file,
            "SEARCH-ERROR": self.search_error
        }

    def run(self):
        search_file_request = SearchFileRequest(self.client.rq, self.file_name)
        self.client.send_message_to_server(search_file_request)

    def search_file(self):
        search_file_response = SearchFileResponse(**bytes_to_object(self.server_response[0]))
        log(search_file_response)
        return True

    def search_error(self):
        search_error = SearchError(**bytes_to_object(self.server_response[0]))
        log(search_error)
        return search_error.reason


class UpdateClientContact(Thread):

    def __init__(self, client, new_ip, new_udp_socket, new_tcp_socket):
        super().__init__()
        self.client = client
        self.new_ip = new_ip
        self.new_udp_socket = new_udp_socket
        self.new_tcp_socket = new_tcp_socket
        self.server_response = None
        self.result = None
        self.response_messages = {
            "UPDATE-CONFIRMED": self.update_confirmed,
            "UPDATE-DENIED": self.update_denied
        }

    def run(self):
        update_contact = UpdateContact(self.client.rq, self.client.name, self.new_ip, self.new_udp_socket, self.new_tcp_socket)
        self.client.send_message_to_server(update_contact)
        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def update_confirmed(self):
        update_confirmed = UpdateConfirmed(**bytes_to_object(self.server_response[0]))
        log(update_confirmed)
        return True

    def update_denied(self):
        update_denied = UpdateDenied(**bytes_to_object(self.server_response[0]))
        log(update_denied)
        return update_denied.reason

class DownloadFileFromPeer(Thread):

    def __init__(self, client, file_name, peer_ip_address, peer_tcp_socket):
        super().__init__()
        self.client = client
        self.file_name = file_name
        self.file_content = ""
        self.peer_ip_address = peer_ip_address
        self.peer_tcp_socket = peer_tcp_socket
        self.peer_response = None

        self.result = None
        self.response_messages = {
            "FILE": self.file,
            "FILE-END": self.file_end,
            "DOWNLOAD-ERROR": self.download_error
        }

    def run(self):
        download = Download(self.client.rq, self.file_name)
        self.client.connect_to_peer(self.peer_ip_address, self.peer_tcp_socket)
        self.client.send_message_to_peer(download)
        self.client.tcp_socket.listen()
        connection, address = self.client.tcp_socket.accept()

        try:
            while True:
                self.peer_response = self.client.tcp_socket.recv(BUFFER_SIZE)
                print(self.peer_response)
                file_transfer_complete = self.response_messages[get_message_type(self.peer_response)]()

                if file_transfer_complete:
                    break

        except socket.error:
            self.result = "Failed to connect to peer."

        self.client.disconnect_from_peer()

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def file(self):
        file = File(**bytes_to_object(self.peer_response))
        self.file_content += file.text
        log(file)
        return False

    def file_end(self):
        file_end = FileEnd(**bytes_to_object(self.peer_response))
        self.file_content += file_end.text
        self.result = True
        log(file_end)
        return True

    def download_error(self):
        download_error = DownloadError(**bytes_to_object(self.peer_response))
        self.result = download_error.reason
        log(download_error)
        return True



